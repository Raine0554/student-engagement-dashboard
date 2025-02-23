import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

from functions.get_spreadsheet_keys import get_spreadsheet_keys
from functions.standardise_headers import standardise_headers

# ------------------------------------------------------------------------------------------*/
# Function to load multiple Google Spreadsheets
def load_multiple_spreadsheets():
    """Fetch and process data from all spreadsheets dynamically."""
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file("event-engagement-dashboard-b9a800641eeb.json", scopes=scope)
    client = gspread.authorize(creds)

    spreadsheets_info = get_spreadsheet_keys()
    all_data = {}

    for sheet_info in spreadsheets_info:
        event_name = sheet_info["event_name"]
        spreadsheet_key = sheet_info["spreadsheet_key"]

        try:
            spreadsheet = client.open_by_key(spreadsheet_key)
            worksheet = spreadsheet.worksheet("Form Responses 1")
            records = worksheet.get_all_records()
            df = pd.DataFrame(records)
            
            # Standardize column names
            df = standardise_headers(df)
            
            all_data[event_name] = df  # Store DataFrame with event name as the key
            
            # {
            #     "Women in Internships": <Pandas DataFrame>,
            #     "Macquarie Technical Workshop": <Pandas DataFrame>,
            #     "Networking Cocktail": <Pandas DataFrame>,
            #     "Emergence": <Pandas DataFrame>
            # }
        
        except Exception as e:
            print(f"Failed to load {event_name} ({spreadsheet_key}): {e}")

    return all_data