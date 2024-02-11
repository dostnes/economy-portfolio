# Base code from https://developers.google.com/sheets/api/quickstart/python

import os.path
import requests
import time
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.exceptions import RefreshError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of the spreadsheet.
SAMPLE_SPREADSHEET_ID = "1J-NvxzITGiWdvbSMk_0OcusLIOVvg1LnrScpjf5rXik"
SAMPLE_RANGE_NAME = "coingecko_data!A2"

def delete_token():
    if os.path.exists("token.json"):
        os.remove("token.json")
        print("Token has been deleted.")
            




# Function that calls Coingecko API
# Paginates through given range
# Calculates API runtime and status code
# Appends timestamp from last runtime 


class CryptoAPIError(Exception):
    pass

def getCryptoAssets():
    base_url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'nok',
        'per_page': 250,
        'page': None 
    }
    #Can add more params from the API.
    myValues = []

    for page in range (1, 3): # This range can be adjusted based on how many pages you want to fetch
        params['page'] = page

        # Record the start time of the API request

        start_time = time.time()

        try:

            response = requests.get(base_url, headers={}, params=params)
            response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)

            data = response.json()

            # Calculate the time taken for the API request
            elapsed_time = time.time() - start_time

            # Print information about the API request
            print(f"API Request - Page {page}")
            print(f"URL: {response.url}")
            print(f"Status Code: {response.status_code}")
            print(f"Time Taken: {elapsed_time:.2f} seconds")

            for item in data:
                myValues.append([
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
            raise CryptoAPIError(f"Error in API request - Page {page}")

    # Append the timestamp to the data
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    myValues.append([f"Last Updated:"])
    myValues.append([timestamp])

    return myValues


def main():
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=3000)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("sheets", "v4", credentials=creds)

    # Run the Coingecko function
    valueData = getCryptoAssets()
    print("------------------------")
    print("Adding data to sheets...")

    # Benchmark time 
    start_time = time.time()
    # Call the Sheets API to update the spreadsheet
    sheet = service.spreadsheets()
    result = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                   range=SAMPLE_RANGE_NAME, valueInputOption="USER_ENTERED", body={"values": valueData}).execute()
    
    # Calculate the time taken for the API request
    elapsed_time = time.time() - start_time

    print("------------------------")
    print(f"Time Taken: {elapsed_time:.2f} seconds")
    print("Success")
    
  except CryptoAPIError as e:
      print("An error occured:", e)
      # If error is raised, stop script
      return
  
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
         with open("token.json", "w") as token:
             token.write(creds.to_json())
      else:
         print("An error ocurred while refreshing the token:", e)

  except HttpError as err:
    print(err)


if __name__ == "__main__":
  main()