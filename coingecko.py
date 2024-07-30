"""
This module interacts with the Google Sheets API to update a spreadsheet with cryptocurrency data
fetched from the Coingecko API.

Functions:
    delete_token(): Deletes the stored token.json file.
    get_crypto_assets(): Fetches cryptocurrency data from the Coingecko API.
    main(): The main function to authenticate with Google Sheets API and update the spreadsheet.

Classes:
    CryptoAPIError: Custom exception for handling errors in the Coingecko API requests.
"""

import os.path
import time
from datetime import datetime
import requests

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.auth.exceptions import RefreshError
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of the spreadsheet.
SAMPLE_SPREADSHEET_ID = "1J-NvxzITGiWdvbSMk_0OcusLIOVvg1LnrScpjf5rXik"
SAMPLE_RANGE_NAME = "coingecko_data!A2"

def delete_token():
    """
    Deletes the stored token.json file if it exists.

    This function checks if the file token.json exists in the current directory.
    If the file is found, it is deleted.
    """
    if os.path.exists("token.json"):
        os.remove("token.json")
        print("Token has been deleted.")

class CryptoAPIError(Exception):
    """
    Custom exception for handling errors in the Coingecko API requests.
    """

def get_crypto_assets():
    """
    Fetches cryptocurrency data from the Coingecko API.

    This function calls the Coingecko API to fetch cryptocurrency market data.
    It paginates through the given range and collects the data, including the
    ID, symbol, name, current price, image URL, and market cap rank. It also
    records the API request time and status code, and appends a timestamp from
    the last runtime.

    Returns:
        list: A list of lists containing cryptocurrency data and a timestamp.
    """
    base_url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'nok',
        'per_page': 250,
        'page': None 
    }
    # Can add more params from the API.
    my_values = []

    for page in range(1, 3):  # This range can be adjusted based on how many pages you want to fetch
        params['page'] = page

        # Record the start time of the API request
        start_time = time.time()

        try:
            response = requests.get(
                base_url,
                headers={},
                params=params,
                timeout=10)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

            data = response.json()

            # Calculate the time taken for the API request
            elapsed_time = time.time() - start_time

            # Print information about the API request
            print(f"API Request - Page {page}")
            print(f"URL: {response.url}")
            print(f"Status Code: {response.status_code}")
            print(f"Time Taken: {elapsed_time:.2f} seconds")

            for item in data:
                my_values.append([
                    item['id'],
                    item['symbol'],
                    item['name'],
                    item['current_price'],
                    item['image'],
                    item['market_cap_rank']
                ])

        except requests.exceptions.RequestException as e:
            # Handle exceptions here
            print(f"Error in API request - Page {page} {e}")
            raise CryptoAPIError(f"Error in API request - Page {page}") from e  # Added `from e`

    # Append the timestamp to the data
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    my_values.append(["Last Updated:"])
    my_values.append([timestamp])

    return my_values

def main():
    """
    The main function to authenticate with Google Sheets API and update the spreadsheet.

    This function handles the authentication with Google Sheets API using OAuth2.
    It fetches cryptocurrency data from the Coingecko API and updates the specified
    Google Sheets spreadsheet with this data. It also handles token expiration and
    refresh errors, and measures the time taken for the API requests.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except RefreshError as e:
                if "invalid_grant" in str(e):
                    # Check if the token has expired or been revoked
                    print("Token has been revoked or expired. Deleting token...")
                    delete_token()
                    print("Rerunning authentication flow...")
                    # Rerun the auth flow
                    flow = InstalledAppFlow.from_client_secrets_file(
                        "credentials.json", SCOPES
                    )
                    creds = flow.run_local_server(port=3000)
                    # Save the new credentials for the next run
                    with open("token.json", "w", encoding="utf-8") as token:
                        token.write(creds.to_json())
                else:
                    print("An error occurred while refreshing the token:", e)
                    return
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=3000)
        # Save the credentials for the next run
        with open("token.json", "w", encoding="utf-8") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)

        # Run the Coingecko function
        value_data = get_crypto_assets()
        print("------------------------")
        print("Adding data to sheets...")

        # Benchmark time
        start_time = time.time()
        # Call the Sheets API to update the spreadsheet
        sheet = service.spreadsheets()  # pylint: disable=no-member
        result = sheet.values().update(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            range=SAMPLE_RANGE_NAME,
            valueInputOption="USER_ENTERED",
            body={"values": value_data}).execute()
        # Calculate the time taken for the API request
        elapsed_time = time.time() - start_time

        print("------------------------")
        print(f"Time Taken: {elapsed_time:.2f} seconds")
        print("SUCCESS")
        print("------------------------")
        print("------------------------")
        print("Result:", result)  # Added print statement for debugging
    except CryptoAPIError as e:
        print("An error occurred:", e)
        # If error is raised, stop script
        return
    except HttpError as err:
        print(err)

if __name__ == "__main__":
    main()
