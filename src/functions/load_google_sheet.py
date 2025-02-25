import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

from functions.get_spreadsheet_keys import get_spreadsheet_keys
from functions.standardise_headers import standardise_headers

def load_forms_spreadsheets():
    """Fetch and process data from all spreadsheets dynamically."""
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file("event-engagement-dashboard-b9a800641eeb.json", scopes=scope)
    client = gspread.authorize(creds)

    spreadsheets_info = get_spreadsheet_keys()
    merged_sheets = spreadsheets_info[0] + spreadsheets_info[1] if isinstance(spreadsheets_info, tuple) else spreadsheets_info
    
    all_data = {}

    for sheet_info in merged_sheets:
        if not isinstance(sheet_info, dict):
            print("Skipping invalid entry:", sheet_info)
            continue

        event_name = sheet_info.get("event_name", "Unknown Event")
        spreadsheet_key = sheet_info.get("spreadsheet_key")

        if not spreadsheet_key:
            print(f"Skipping {event_name}: Missing spreadsheet key")
            continue

        try:
            spreadsheet = client.open_by_key(spreadsheet_key)
            worksheet = spreadsheet.worksheet("Form Responses 1")
            records = worksheet.get_all_records()
            df = pd.DataFrame(records)

            # Standardize column names
            df = standardise_headers(df)

            all_data[event_name] = df  # Store DataFrame with event name as key
        
        except gspread.exceptions.APIError as api_error:
            print(f"API error while loading {event_name} ({spreadsheet_key}): {api_error}")
        except gspread.exceptions.SpreadsheetNotFound:
            print(f"Spreadsheet not found: {event_name} ({spreadsheet_key})")
        except Exception as e:
            print(f"Unexpected error loading {event_name} ({spreadsheet_key}): {e}")

    return all_data
