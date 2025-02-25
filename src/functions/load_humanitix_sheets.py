import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

from functions.get_spreadsheet_keys import get_spreadsheet_keys

# ------------------------------------------------------------------------------------------*/
# Function to load multiple Google Spreadsheets
def load_humanitix_spreadsheets():
    """Fetch and process data from all spreadsheets dynamically."""
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file("event-engagement-dashboard-b9a800641eeb.json", scopes=scope)
    client = gspread.authorize(creds)

    spreadsheets_info = get_spreadsheet_keys()
    all_data = {}

    for sheet_info in spreadsheets_info[1]:
        name = sheet_info["name"]
        spreadsheet_key = sheet_info["spreadsheet_key"]

        try:
            spreadsheet = client.open_by_key(spreadsheet_key)
            worksheet = spreadsheet.worksheet("Sheet1")
            records = worksheet.get_all_records()
            df = pd.DataFrame(records)
            
            
            all_data[name] = df  # Store DataFrame with event name as the key
            
            # {
            #     "event-report": <Pandas DataFrame>,
            #     "attendee-report Technical Workshop": <Pandas DataFrame>,
            # }
        
        except Exception as e:
            print(f"Failed to load {name} ({spreadsheet_key}): {e}")

    return all_data