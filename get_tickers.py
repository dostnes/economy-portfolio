"""
Connects to Google Sheets, fetches stock tickers, and saves them
to a file named tickers.txt, one ticker per line.
"""
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1J-NvxzITGiWdvbSMk_0OcusLIOVvg1LnrScpjf5rXik"
DATA_RANGE = "Ark!C6:G28"

def main():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=3000)
        with open("token.json", "w", encoding="utf-8") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=DATA_RANGE).execute()
        rows = result.get("values", [])

        if not rows:
            print("No data found in the specified range.")
            return

        tickers = []
        for row in rows:
            if len(row) >= 5 and row[0].strip() == "ASK 2 - Stock":
                ticker = row[4].strip()
                if ticker:
                    tickers.append(ticker)
        
        if tickers:
            with open("tickers.txt", "w", encoding="utf-8") as f:
                for ticker in tickers:
                    f.write(f"{ticker}\n")
            print(f"✅ Successfully saved {len(tickers)} tickers to tickers.txt.")
        else:
            print("❌ No matching stocks found to save.")

    except HttpError as err:
        print(f"A Google Sheets API error occurred: {err}")

if __name__ == "__main__":
    main()