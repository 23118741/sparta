import os
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

class GoogleSheetsConfig:
    """Verantwoordelijk voor de inloggegevens en API-verbindingen."""
    def __init__(self):
        self.gmail_user = os.getenv("GMAIL_USER")
        self.gmail_password = os.getenv("GMAIL_PASSWORD")
        self.spreadsheet_id = os.getenv("SPREADSHEET_ID")
        
        self.scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        self.creds = Credentials.from_service_account_file("credentials.json", scopes=self.scopes)
        self.client = gspread.authorize(self.creds)
        self.spreadsheet = self.client.open_by_key(self.spreadsheet_id)
        self.sheet = self.spreadsheet.sheet1
        try:
            self.wachtlijst_sheet = self.spreadsheet.worksheet("wachtlijst")
        except gspread.exceptions.WorksheetNotFound:
            print("Waarschuwing: Worksheet 'wachtlijst' niet gevonden.")
            self.wachtlijst_sheet = None