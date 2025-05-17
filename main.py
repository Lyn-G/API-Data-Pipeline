import os
from dotenv import load_dotenv
import requests
import gspread
from google.oauth2.service_account import Credentials

# Load environment variables
load_dotenv()

# Get from .env
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds_path = os.getenv("GOOGLE_CREDS_PATH")

creds = Credentials.from_service_account_file(creds_path, scopes=scopes)
client = gspread.authorize(creds)

sheet_id = os.getenv("GOOGLE_SHEET_ID")
sheet = client.open_by_key(sheet_id)

values_list = sheet.sheet1.row_values(1)
print(values_list)

# response = requests.get("https://api.example.com/data")


class BaseAPI:
    def __init__(self, baseurl, apikey=""):
        self.baseurl = baseurl
        self.apikey = apikey

    def get(self, endpoint=""):
        r = requests.get(self.baseurl + endpoint)
        return r.json()
        
