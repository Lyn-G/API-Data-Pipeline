import os
from dotenv import load_dotenv
import requests
import gspread
from google.oauth2.service_account import Credentials

# load super secret information !
# necessary to push to Git since i'm working with APIs
load_dotenv()

# authenticating access
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
creds_path = os.getenv("GOOGLE_CREDS_PATH")

creds = Credentials.from_service_account_file(creds_path, scopes=scopes)
client = gspread.authorize(creds)


# start of the classes
class BaseAPI:
    def __init__(self, baseurl):
        self.baseurl = baseurl

    def get(self, endpoint=""):
        url = self.baseurl + endpoint
        response = requests.get(url)
        response.raise_for_status()
        return response.json()


class YuGiOhAPI(BaseAPI):
    def __init__(self):
        super().__init__("https://db.ygoprodeck.com/api/v7")

    def GetCards(self, archetype):
        # search up card archetypes
        data = self.get(f"/cardinfo.php?archetype={archetype}")
        cards = []

        for card in data.get("data", [])[:]:
            cards.append(
                {
                    "name": card.get("name"),
                    "type": card.get("type"),
                    "desc": card.get("desc", "")[:100] + "...",
                    "image_url": card.get("card_images", [{}])[0].get("image_url", ""),
                }
            )

        return cards


def GetorCreateSheet(sheet_title, emails=None):
    # check if sheet exists. if not, create a new one
    try:
        sheet = client.open(sheet_title)
        sheet.values_clear()
        print("Editing existing sheet.")
    except gspread.SpreadsheetNotFound:
        sheet = client.create(sheet_title)
        print("Creating new sheet.")

    # share sheet to email addresses
    if emails:
        for email in emails:
            sheet.share(email, perm_type="user", role="writer")

    return sheet


def WriteToSheet(data, sheet):
    worksheet = sheet.sheet1

    # get headers from keys in dictionary
    headers = list(data[0].keys())
    values = [headers] + [[row[h] for h in headers] for row in data]

    worksheet.update(values, "A1")


if __name__ == "__main__":
    yugioh = YuGiOhAPI()
    email_addresses = ["lexicolorful@gmail.com"]

    sheet = GetorCreateSheet("Crypto Prices", emails=email_addresses)

    cards = yugioh.GetCards("Dark Magician")

    WriteToSheet(cards, sheet)
