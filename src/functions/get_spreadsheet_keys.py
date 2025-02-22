import json

# Function to read spreadsheet keys and event names from JSON
def get_spreadsheet_keys():
    """Read spreadsheet keys and event names from a JSON file."""
    with open("spreadsheets.json", "r") as file:
        data = json.load(file)
    return data["spreadsheets"]  # Returns a list of dictionaries
