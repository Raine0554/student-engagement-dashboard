import json

# Function to read spreadsheet keys and event names from JSON
def get_spreadsheet_keys():
    """Read spreadsheet keys and event names from two JSON files."""
    with open("forms-spreadsheets.json", "r") as file1:
        data1 = json.load(file1)

    with open("humanitix-spreadsheets.json", "r") as file2:
        data2 = json.load(file2)

    return data1["spreadsheets"], data2["spreadsheets"]  # Returns two separate lists
