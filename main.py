import os
from dotenv import load_dotenv
import requests
import gspread
from google.oauth2.service_account import Credentials

# load super secret information !
# necessary to push to Git using APIs
load_dotenv()

# authenticating access
scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
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


class CryptoAPI(BaseAPI):
    def __init__(self):
        super().__init__("https://api.coingecko.com/api/v3")

    def GetTopCoins(self, limit=5):
        data = self.get("/coins/markets?vs_currency=usd")

        # transform — grab the top coins
        cleaned = [
            {
                "name": coin["name"],
                "symbol": coin["symbol"],
                "price": coin["current_price"],
            }
            for coin in data[:limit]
        ]
        return cleaned
    
def GetorCreateSheet(sheet_title, emails=None):
    # check if sheet exists. if not, create a new one
    try:
        sheet = client.open(sheet_title)
        print("Editing existing sheet.")
    except gspread.SpreadsheetNotFound:
        sheet = client.create(sheet_title)
        print("Creating new sheet.")
    
    # Share spreadsheets to email addresses
    if emails:
        for email in emails:
            sheet.share(email, perm_type='user', role='writer')

    return sheet

def WriteToSheet(data, sheet):
    worksheet = sheet.sheet1

    # get headers from keys of the first dictionary
    headers = list(data[0].keys())
    values = [headers] + [[row[h] for h in headers] for row in data]

    worksheet.update(values, "A1")




if __name__ == "__main__":
    crypto = CryptoAPI()
    email_addresses = ["lexicolorful@gmail.com"]
    
    sheet = GetorCreateSheet("Crypto Prices", emails=email_addresses)

    top_coins = crypto.GetTopCoins(limit=10)
    WriteToSheet(top_coins, sheet)
