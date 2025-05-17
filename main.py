import os
from dotenv import load_dotenv
import requests
import gspread
from google.oauth2.service_account import Credentials

# load super secret information !
# necessary to push to Git using APIs
load_dotenv()

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds_path = os.getenv("GOOGLE_CREDS_PATH")

creds = Credentials.from_service_account_file(creds_path, scopes=scopes)
client = gspread.authorize(creds)

# open up Google Sheets
sheet_id = os.getenv("GOOGLE_SHEET_ID")
sheet = client.open_by_key(sheet_id)  

# response = requests.get("https://api.example.com/data")


class BaseAPI:
    def __init__(self, baseurl, apikey=""):
        self.baseurl = baseurl
        self.apikey = apikey

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
        cleaned = [{
            "name": coin["name"],
            "symbol": coin["symbol"],
            "price": coin["current_price"]
        } for coin in data[:limit]]
        return cleaned

def WriteToSheet(data, sheet_name="Sheet1"):
    worksheet = sheet.worksheet(sheet_name)

    if not data:
        print("No data to write.")
        return

    # Get headers from keys of the first dictionary
    headers = list(data[0].keys())
    values = [headers] + [[row[h] for h in headers] for row in data]

    worksheet.update(values, "A1")

if __name__ == "__main__":
    crypto = CryptoAPI()
    top_coins = crypto.GetTopCoins(limit=5)
    WriteToSheet(top_coins, sheet_name="Sheet1")
