import os
from dotenv import load_dotenv
import requests
import gspread
from google.oauth2.service_account import Credentials

# load super secret information !
# necessary to push to Git since i'm working with APIs
load_dotenv()

# authenticating access
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
CREDS_PATH = os.getenv("GOOGLE_CREDS_PATH")

CREDS = Credentials.from_service_account_file(CREDS_PATH, scopes=SCOPES)
CLIENT = gspread.authorize(CREDS)


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

    def get_cards(self, archetype=None):
        try:
            # default to Dark Magician if nothing put in
            archetype = archetype or "Dark Magician"

            # search up card archetypes
            data = self.get(f"/cardinfo.php?archetype={archetype}")
            card_to_sheets = []

            for card in data.get("data"):
                card_data = self._card_data(card)
                card_to_sheets.append(card_data)

            # sort and return top 15 cards by power source
            card_to_sheets.sort(key=lambda card: card["Power Score"], reverse=True)
            return card_to_sheets[:15]

        # quit program if archetype not found
        except:
            print("\nI couldn't find that archetype...\nPlease try again.")
            quit()

    def _card_data(self, card):
        return {
            "Name": card.get("name"),
            "Type": card.get("type"),
            "Power Score": self._get_power_score(card),
            "Description": self._get_description(card.get("desc")),
            "Image Url": self._get_image_url(card),
        }

    def _get_description(self, desc, length=100):
        return desc[:length] + "..." if len(desc) > length else desc

    def _get_power_score(self, card):
        attack = card.get("atk", 0)
        defense = card.get("def", 0)

        power_score = (attack + defense) / 2
        return round(power_score, 1)

    def _get_image_url(self, card):
        return card.get("card_images", [{}])[0].get("image_url")


# start of the global functions
def get_or_create_sheet(sheet_title, emails=None):
    # check if sheet exists. if not, create a new one
    try:
        sheet = CLIENT.open(sheet_title)
        print("\nSheet name found! Let me edit that for you!\n")
    except gspread.SpreadsheetNotFound:
        sheet = CLIENT.create(sheet_title)
        print("\nA new sheet name? Creating and editing new sheet!\n")

    # share sheet to email addresses
    if emails:
        already_shared = [
            p.get("emailAddress").lower()
            for p in sheet.list_permissions()
            if p.get("emailAddress")
        ]

        for email in emails:
            if email not in already_shared:
                # if the user did not add in an actual email
                try: 
                    sheet.share(email, perm_type="user", role="writer")
                    print(f"Sharing with {email}.")
                except:
                    print(f"{email} could not be shared to the sheet.")
            else:
                print(f"Already shared with {email}.")

    return sheet


def write_to_sheet(data, sheet):
    worksheet = sheet.sheet1
    worksheet.clear()

    # get headers from keys in dictionary
    headers = list(data[0].keys())
    values = [headers] + [[row[h] for h in headers] for row in data]

    worksheet.update(values, "A1")
    print("\nHere is the top 15 strongest cards for that archetype!\nClick the link below!")
    print(f"https://docs.google.com/spreadsheets/d/{sheet.id}")


if __name__ == "__main__":
    yugioh = YuGiOhAPI()

    email_addresses = []
    print("\nBefore we get started,")

    while True:
        ask_email = input("\nWhat email would you like to share your sheet to?\n"
        "Type   n   to let me know you finished!\n")
        
        if (ask_email.lower() == "n"): break

        email_addresses.append(ask_email.lower())

    sheet = get_or_create_sheet(
        input("What would you like to name your sheet?  "), emails=email_addresses
    )

    archetypes = input(
        "\nWhat archetype would you like to find information for?\n"
        "https://db.ygoprodeck.com/api/v7/archetypes.php\n"
        "Default shall be Dark Magician.\n"
    )

    cards = yugioh.get_cards(archetypes)
    write_to_sheet(cards, sheet)
