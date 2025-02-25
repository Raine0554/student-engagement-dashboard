import pandas as pd

# importing fuctions for data processing
from functions.categorise_events import categorise_event
from functions.standardise_headers import standardise_headers
from functions.load_google_sheet import load_forms_spreadsheets


# ------------------------------------------------------------------------------------------*/
# DATA PROCESSING


def process_data():
    # Automatically load spreadsheets into a list of dictionaries
    sheets_data = load_forms_spreadsheets()
    
    # Creating a custom dataframe with processed values
    processed_data = []
    for event_name, df in sheets_data.items():
        # Ensure "Event Rating" exists before applying mean()
        if "Event Rating" in df.columns:
            df["Event Rating"] = pd.to_numeric(df["Event Rating"], errors="coerce")  # Convert to numeric safely
            avg_rating = df["Event Rating"].mean()
        else:
            avg_rating = None  # Assign None if column is missing
        # total_attendance = df["Attendance"].sum()

        event_type = categorise_event(event_name)  # Reusing event categorization function

        processed_data.append({
            "Event Name": event_name,
            "Event Type": event_type,
            "Avg Event Rating": round(avg_rating, 2),
            # "Attendance No.": total_attendance
        })

    # Convert to DataFrame
    df_processed = pd.DataFrame(processed_data)

    return df_processed