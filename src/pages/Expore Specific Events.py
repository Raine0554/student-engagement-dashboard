import streamlit as st
import pandas as pd
from textblob import TextBlob
from sklearn.linear_model import LinearRegression
import numpy as np

# # Sidebar dropdown to select an event by name
# selected_event = st.sidebar.selectbox("Select a Specific Event", list(sheets_data.keys()))
# # event_type = st.sidebar.selectbox("Select Event Type")

# # Display DataFrame from the selected event
# df = sheets_data[selected_event]
# st.subheader(f"📋 Data from {selected_event}", )
# st.dataframe(df)

from functions.process_data import process_data
from functions.load_google_sheet import load_multiple_spreadsheets

# ------------------------------------------------------------------------------------------*/
# Loading the data

sheets_data = load_multiple_spreadsheets()
df_processed = process_data()

# ------------------------------------------------------------------------------------------*/

st.markdown("---")
st.subheader("🔭 Explore Specific Events")

# Dropdown to select an event by name
selected_event = st.selectbox("Select a Specific Event", list(sheets_data.keys()))

# event_type = st.sidebar.selectbox("Select Event Type")

# Display DataFrame from the selected event
df = sheets_data[selected_event]
st.subheader(f"📋 Data from {selected_event}", )
st.dataframe(df)

# Average Rating
st.subheader("⭐ Average Event Rating")
if "Event Rating" in df.columns:
    df["Event Rating"] = pd.to_numeric(df["Event Rating"], errors="coerce")
    st.metric("Average Event Rating", round(df["Event Rating"].mean(), 2))

# Recommendation Score
st.subheader("📢 Recommendation Likelihood")
if "Recommendation Score" in df.columns:
    df["Recommendation Score"] = pd.to_numeric(df["Recommendation Score"], errors="coerce")
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