import streamlit as st
import pandas as pd
from textblob import TextBlob
from sklearn.linear_model import LinearRegression
import numpy as np


st.set_page_config(
    page_title="My App",  # Change this to your app title
    page_icon="🔭",  # Optional: Set an emoji or image as favicon
    layout="centered"  # Ensures content is not full-width
)

page_bg = """
<style>
    /* Change main page background */
    .stApp {
        background-color: #212751; /* Light gray */
    }

    /* Change sidebar background */
    section[data-testid="stSidebar"] {
        background-color: #1A1A3D; /* Light blue-gray */
    }

    /* Change top navbar (Streamlit menu bar) */
    header[data-testid="stHeader"] {
        background-color: #212751; /* Darker blue */
    }

    /* Change font color in the navbar */
    header[data-testid="stHeader"] * {
        color: white; /* Change text/icon color to white */
    }
</style>
"""

st.markdown(page_bg, unsafe_allow_html=True)

# # Sidebar dropdown to select an event by name
# selected_event = st.sidebar.selectbox("Select a Specific Event", list(sheets_data.keys()))
# # event_type = st.sidebar.selectbox("Select Event Type")

# # Display DataFrame from the selected event
# df = sheets_data[selected_event]
# st.subheader(f"📋 Data from {selected_event}", )
# st.dataframe(df)

from functions.process_data import process_data
from functions.load_google_sheet import load_forms_spreadsheets
from functions.load_humanitix_sheets import load_humanitix_spreadsheets

# ------------------------------------------------------------------------------------------*/
# Loading the data

google_forms_data = load_forms_spreadsheets()
humanitix_data = load_humanitix_spreadsheets()
print(humanitix_data)

# ------------------------------------------------------------------------------------------*/



# ------------------------------------------------------------------------------------------*/
# PROCESS HUMANITIX DATA

# To prevent Streamlit from resetting humanitix_data, store it in st.session_state:
# Load data only once and store it in session state
if "humanitix_data" not in st.session_state:
    from functions.load_humanitix_sheets import load_humanitix_spreadsheets
    st.session_state.humanitix_data = load_humanitix_spreadsheets()  # Save it persistently

# Access data from session state
humanitix_data = st.session_state.humanitix_data

# Debugging: Check if "events-report" exists
if "events-report" not in humanitix_data:
    st.error("❌ 'events-report' is missing from Humanitix data. Check API response.")
    st.stop()  # Stop execution to avoid further errors

# ------------------------------------------------------------------------------------------*/
# FILTER DATA BY EVENT NAME SELECTED

event_data = humanitix_data["events-report"]
attendee_data = humanitix_data["attendee-report"]

# Normalize event names to avoid case-sensitivity and trailing spaces
event_data["Event Name"] = event_data["Event Name"].str.strip().str.lower()
event_names = event_data["Event Name"].unique()  # Get unique event names


st.title("🔭 Explore Specific Events")
# Select an event
selected_event = st.selectbox("Select a Specific Event", event_names)

# Ensure the selected event is case-insensitive and space-normalized
filtered_row = event_data[event_data["Event Name"].str.lower() == selected_event.lower()]

# ------------------------------------------------------------------------------------------*/
# BASIC EVENT INFO - WORKS

attendance = filtered_row["Sold"].values[0]  # Get the first matching value
st.write(f"Tickets Sold: {attendance}")

location = filtered_row["Location"].values[0]  # Get the first matching value
st.write(f"📍 Location: {location}")
    
date = filtered_row["Date"].values[0]  # Get the first matching value
st.write(f"📅 Date: {date}")

time = filtered_row["Time"].values[0]  # Get the first matching value
st.write(f"⏰ Time: {time}")


# ------------------------------------------------------------------------------------------*/

st.markdown("---")



# event_type = st.sidebar.selectbox("Select Event Type")

# Display DataFrame from the selected event
df = google_forms_data[selected_event]
st.subheader(f"📋 Basic stats from {selected_event}", )

# if "Event Rating" in df.columns:
#     df["Event Rating"] = pd.to_numeric(df["Event Rating"], errors="coerce")
#     st.metric("Average Event Rating", round(df["Event Rating"].mean(), 2))

# Define colored box template
def colored_box(label, value, color):
    return f"""
    <div style="background-color: {color}; padding: 15px; border-radius: 10px; text-align: center; width: 150px; font-size: 16px; font-weight: bold; color: white;">
        {label}<br><span style="font-size: 20px;">{value}</span>
    </div>
    """

# Arrange boxes in a row using columns
col1, col2, col3, col4 = st.columns(4)

# Display each metric with a colored box
with col1:
    st.markdown(colored_box("Total Events", event_rating, "#3498db"), unsafe_allow_html=True)
with col2:
    st.markdown(colored_box("Highest Rating", highest_rating, "#2ecc71"), unsafe_allow_html=True)
with col3:
    st.markdown(colored_box("Lowest Rating", lowest_rating, "#e74c3c"), unsafe_allow_html=True)
with col4:
    st.markdown(colored_box("Average Rating", average_rating, "#f39c12"), unsafe_allow_html=True)
# Average Rating






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