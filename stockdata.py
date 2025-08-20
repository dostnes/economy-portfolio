"""
This script connects to the Google Sheets API to fetch stock data.

It reads a specified range, filters rows based on a condition in one
column, and prints the collected stock names and tickers.
"""
import os.path
import yfinance as yf
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# --- IMPORTANT: UPDATE THESE VALUES ---
# The ID of your spreadsheet (from the URL)
SPREADSHEET_ID = "1J-NvxzITGiWdvbSMk_0OcusLIOVvg1LnrScpjf5rXik"
# The name of your sheet and the range to read.
# Format: "SheetName!StartCell:EndCell"
DATA_RANGE = "Equities Nordnet & Unlisted!C6:G28"
# -------------------------------------

def main():
    """
    Authenticates with the Google Sheets API, fetches data, and prints
    stock tickers and names that match the specified criteria.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=3000)
        # Save the credentials for the next run
        with open("token.json", "w", encoding="utf-8") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API to read the data
        sheet = service.spreadsheets() # pylint: disable=no-member
        result = (
            sheet.values()
            .get(spreadsheetId=SPREADSHEET_ID, range=DATA_RANGE)
            .execute()
        )
        rows = result.get("values", [])

        if not rows:
            print("No data found in the specified range.")
            return

        print("--- Checking for matching stocks ---")
        collected_stocks = []
        for row in rows:
            # Ensure the row has enough columns to avoid errors
            # C=0, D=1, E=2, F=3, G=4 (relative to the range C:G)
            if len(row) < 5:
                continue

            # Get values from columns, using .strip() to remove extra whitespace
            condition_value = row[0].strip() # Column C
            stock_name = row[1].strip()      # Column D
            stock_ticker = row[4].strip()    # Column G

            # Check if the condition in Column C is met
            if condition_value == "ASK 2 - Stock":
                collected_stocks.append({"name": stock_name, "ticker": stock_ticker})

        # Print the collected stocks
        if collected_stocks:
            print("\n✅ Found the following stocks matching 'ASK 2 - Stock':")
            for stock in collected_stocks:
                print(f"  - Name: {stock['name']}, Ticker: {stock['ticker']}")
        else:
            print("\n❌ No stocks found with the condition 'ASK 2 - Stock'.")
            return # Exit if no stocks found
        # Get stock data using yfinance
        print("\n--- Fetching stock data using yfinance ---")
        for stock in collected_stocks:
            original_ticker = stock["ticker"]

            ticker_for_yfinance = original_ticker + ".OL"  # Append .OL for Oslo Stock Exchange

            try:
                ticker_data = yf.Ticker(ticker_for_yfinance)
                hist = ticker_data.history(period="1mo")

                if not hist.empty:
                    latest_price = hist['Close'].tail()  # Get the latest closing price
                    print(f"Ticker: {ticker_for_yfinance}, Latest Price: {latest_price}")
                else:
                    print(f"Ticker: {ticker_for_yfinance} has no data available.")
            except (KeyError, IndexError) as e:
                print(f"Error processing data for {ticker_for_yfinance}: {e}")
            except Exception as e:
                print(f"Unexpected error fetching data for {ticker_for_yfinance}: {e}")


    except HttpError as err:
        print(f"An error occurred: {err}")
    except FileNotFoundError:
        # This long print statement has been split across two lines.
        print(
            "Error: credentials.json not found. "
            "Please ensure the file is in the correct directory."
        )


if __name__ == "__main__":
    main()
