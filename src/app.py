import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from textblob import TextBlob
from sklearn.linear_model import LinearRegression
import numpy as np

# Google Sheets API Setup
def load_data():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file("event-engagement-dashboard-b9a800641eeb.json", scopes=scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key("1mNScnRSIOcKGFjGl31XTgSEkttaStMFy6bd1Jw0KJTY")
    worksheet = spreadsheet.worksheet("Form Responses 1")  # Ensure correct sheet name

    data = worksheet.get_all_records()
    df = pd.DataFrame(data)

    # Rename headers for better readability
    df.rename(columns={
        "Overall, how would you rate this event?": "Event Rating",
        "How do you think this event has improved your knowledge in getting an internship? ": "Internship Knowledge Gain",
        "How did you think of the registration, ticketing experience? ": "Registration Experience",
        "How did you feel about the communication before, during and after the event? \n\n(e.g. receiving emails, communication and instruction given prior and during the event)": "Communication Rating",
        "Which parts of the event did you like the most?": "Best Parts",
        "Which parts of the event do you think can be improved on?": "Improvement Areas",
        "How did you think of the food? ": "Food Rating",
        "What are some topics / domains that you would like to hear about in our upcoming Women In X events? \n\n(e.g. Software Engineering, Cyber Security, UI/UX...etc.) ": "Future Topics",
        "Any overall comment or suggestion?": "Feedback Comments",
        "How likely is it that you would recommend the event to a friend or a peer?": "Recommendation Score"
    }, inplace=True)

    return df

df = load_data()

st.title("📊 Student Event Engagement Dashboard")

# Display Filtered Data
st.subheader("📋 Event Feedback Data")
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
