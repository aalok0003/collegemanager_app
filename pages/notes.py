import streamlit as st
import pandas as pd
from datetime import datetime
import pymongo

# Connect to MongoDB Atlas
# Replace 'YOUR_CONNECTION_STRING' with your actual MongoDB Atlas connection string
client = pymongo.MongoClient('mongodb+srv://aalok:aalok@cluster0.cgn9day.mongodb.net/?retryWrites=true&w=majority')
db = client['class_notes']  # Replace 'attendance_db' with your preferred database name
collection = db['class_notes']

st.title("Add Class Notes")

# Get the current date from the device
current_date = datetime.now().date()

subject = st.selectbox("Select Subject", ("Network Security and Cryptography", "Data Mining and Data Warehousing", "Elective-4", "Elective-5"),key="subject_selector")

# Set the default value of the date input widget to the current date
selected_date = st.date_input("Select Date", value=current_date, key="date_selector")

# Add your notes for the selected subject and date
notes = st.text_area("Add Notes")

# Save the notes data to the database
if st.button("Submit"):
    your_notes_data = {
        "subject": subject,
        "date": selected_date.strftime("%Y-%m-%d"),
        "attended": notes,
    }
    collection.insert_one(your_notes_data)
    st.success("Notes data saved successfully!")



# Add a button to download all your attendance data as a CSV file
if st.button("Fetch All Notes Data"):
    all_notes_data = collection.find()
    all_data_list = list(all_notes_data)
    if all_data_list:
        df = pd.DataFrame(all_data_list)
        st.dataframe(df)
        df.to_csv("your_notes_data.csv", index=False)
        st.success("Notes data downloaded successfully!")
    else:
        st.warning("No notes data found to download.")
