import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from textblob import TextBlob
from sklearn.linear_model import LinearRegression
import numpy as np
import json

# Function to read spreadsheet keys and event names from JSON
def get_spreadsheets_from_json():
    """Read spreadsheet keys and event names from a JSON file."""
    with open("spreadsheets.json", "r") as file:
        data = json.load(file)
    return data["spreadsheets"]  # Returns a list of dictionaries

# Function to load multiple Google Spreadsheets
def load_multiple_spreadsheets():
    """Fetch and process data from all spreadsheets dynamically."""
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file("event-engagement-dashboard-b9a800641eeb.json", scopes=scope)
    client = gspread.authorize(creds)

    spreadsheets_info = get_spreadsheets_from_json()
    all_data = {}

    for sheet_info in spreadsheets_info:
        event_name = sheet_info["event_name"]
        spreadsheet_key = sheet_info["spreadsheet_key"]

        try:
            spreadsheet = client.open_by_key(spreadsheet_key)
            worksheet = spreadsheet.worksheet("Form Responses 1")
            records = worksheet.get_all_records()
            df = pd.DataFrame(records)
            all_data[event_name] = df  # Store DataFrame with event name as the key
        except Exception as e:
            print(f"Failed to load {event_name} ({spreadsheet_key}): {e}")

    return all_data

# Automatically load spreadsheets
sheets_data = load_multiple_spreadsheets()

st.title("💻 WIT Event Engagement Dashboard")

# Sidebar dropdown to select an event by name
selected_event = st.sidebar.selectbox("Select an Event", list(sheets_data.keys()))

# Display DataFrame from the selected event
df = sheets_data[selected_event]
st.subheader(f"📋 Data from {selected_event}")
st.dataframe(df)

# Average Rating and Recommendation Score
st.subheader("⭐ Event Satisfaction Overview")
if "Event Rating" in df.columns and "Recommendation Score" in df.columns:
    df["Event Rating"] = pd.to_numeric(df["Event Rating"], errors="coerce")
    df["Recommendation Score"] = pd.to_numeric(df["Recommendation Score"], errors="coerce")
    st.metric("Average Event Rating", round(df["Event Rating"].mean(), 2))
    st.metric("Recommendation Likelihood", round(df["Recommendation Score"].mean(), 2))

# Sentiment Analysis on Feedback
if "Feedback Comments" in df.columns:
    st.subheader("💬 Sentiment Analysis on Feedback")
    df["Sentiment"] = df["Feedback Comments"].dropna().apply(lambda x: TextBlob(str(x)).sentiment.polarity)
    st.bar_chart(df.groupby("Event Rating")["Sentiment"].mean())

# Future Event Topics Insights
if "Future Topics" in df.columns:
    st.subheader("📌 Suggested Future Topics")
    topic_counts = df["Future Topics"].dropna().str.split(",").explode().str.strip().value_counts()
    st.bar_chart(topic_counts)

st.success("Dashboard successfully loaded! 🎉")



# # Google Sheets API Setup
# def load_data():
#     scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
#     creds = Credentials.from_service_account_file("event-engagement-dashboard-b9a800641eeb.json", scopes=scope)
#     client = gspread.authorize(creds)
#     spreadsheet = client.open_by_key("1mNScnRSIOcKGFjGl31XTgSEkttaStMFy6bd1Jw0KJTY")
#     worksheet = spreadsheet.worksheet("Form Responses 1")  # Ensure correct sheet name
#     data = worksheet.get_all_records()
#     df = pd.DataFrame(data)

#     # Rename headers for better readability
#     df.rename(columns={
#         "Overall, how would you rate this event?": "Event Rating",
#         "How do you think this event has improved your knowledge in getting an internship? ": "Internship Knowledge Gain",
#         "How did you think of the registration, ticketing experience? ": "Registration Experience",
#         "How did you feel about the communication before, during and after the event? \n\n(e.g. receiving emails, communication and instruction given prior and during the event)": "Communication Rating",
#         "Which parts of the event did you like the most?": "Best Parts",
#         "Which parts of the event do you think can be improved on?": "Improvement Areas",
#         "How did you think of the food? ": "Food Rating",
#         "What are some topics / domains that you would like to hear about in our upcoming Women In X events? \n\n(e.g. Software Engineering, Cyber Security, UI/UX...etc.) ": "Future Topics",
#         "Any overall comment or suggestion?": "Feedback Comments",
#         "How likely is it that you would recommend the event to a friend or a peer?": "Recommendation Score"
#     }, inplace=True)

#     return df

# df = load_data()