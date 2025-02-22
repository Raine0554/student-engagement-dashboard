import difflib

COLUMN_MAPPING = {
    "Event Rating": ["Event Rating", "Overall Rating", "Rating", "How would you rate this event?"],
    "Registration Experience": ["Registration Experience", "Ticketing Experience", "How was the registration process?"],
    "Communication Rating": ["Communication Rating", "Email Communication", "How did you feel about communication?"],
    "Best Parts": ["Best Parts", "What did you like about the event?", "Favorite Aspects"],
    "Improvement Areas": ["Improvement Areas", "What can be improved?", "Suggestions for Improvement"],
    "Food Rating": ["Food Rating", "How was the food?", "Catering Feedback"],
    "Future Topics": ["Future Topics", "Topics of Interest", "What topics would you like to see?"],
    "Feedback Comments": ["Feedback Comments", "General Comments", "Any overall comment or suggestion?"],
    "Recommendation Score": ["Recommendation Score", "Would you recommend?", "Likelihood to Recommend"]
}

# Function to auto-match inconsistent column headers to pre-defined header names
def standardise_headers(df):
    """Rename columns in the DataFrame to match standard headers."""
    new_columns = {}
    
    for col in df.columns:
        col_cleaned = col.strip().lower()  # Remove spaces & convert to lowercase
        matched_header = None

        for standard_name, variations in COLUMN_MAPPING.items():
            # Normalize variations for comparison
            normalized_variations = [v.strip().lower() for v in variations]

            if col_cleaned in normalized_variations:
                matched_header = standard_name
                break

        # Fuzzy match if no exact match found
        if not matched_header:
            for standard_name, variations in COLUMN_MAPPING.items():
                close_matches = difflib.get_close_matches(col_cleaned, [v.lower() for v in variations], n=1, cutoff=0.6)
                if close_matches:
                    matched_header = standard_name
                    break

        # If still no match, keep original column name
        new_columns[col] = matched_header if matched_header else col

    df.rename(columns=new_columns, inplace=True)
    return df
