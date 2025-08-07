import gspread
from google.oauth2.service_account import Credentials
import os

def get_sheet(sheet_id, sheet_name):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    
    creds_path = os.path.join(os.path.dirname(__file__), "service_account.json")
    if not os.path.exists(creds_path):
        raise FileNotFoundError(f"Service account file not found: {creds_path}")
    
    creds = Credentials.from_service_account_file(creds_path, scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(sheet_id).worksheet(sheet_name)
    return sheet
