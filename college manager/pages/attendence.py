import streamlit as st
import pandas as pd
from datetime import datetime
import pymongo

# Connect to MongoDB Atlas
# Replace 'YOUR_CONNECTION_STRING' with your actual MongoDB Atlas connection string
client = pymongo.MongoClient('mongodb+srv://aalok:aalok@cluster0.cgn9day.mongodb.net/?retryWrites=true&w=majority')
db = client['attendance_db']  # Replace 'attendance_db' with your preferred database name
collection = db['attendance_data']

st.title("Update Your Attendance")

# Get the current date from the device
current_date = datetime.now().date()

subject = st.selectbox("Select Subject", ("Network Security and Cryptography", "Data Mining and Data Warehousing", "Elective-4", "Elective-5"))

# Set the default value of the date input widget to the current date
selected_date = st.date_input("Select Date", value=current_date)

# Mark your attendance for the selected subject and date
attended = st.checkbox("Attended", value=False)

# Save the attendance data to the database
if st.button("Submit"):
    your_attendance_data = {
        "subject": subject,
        "date": selected_date.strftime("%Y-%m-%d"),
        "attended": attended,
    }
    collection.insert_one(your_attendance_data)
    st.success("Attendance data saved successfully!")



# Add a button to download all your attendance data as a CSV file
if st.button("Fetch All Attendance Data"):
    your_attendance_data = collection.find()
    all_data_list = list(your_attendance_data)
    if all_data_list:
        df = pd.DataFrame(all_data_list)
        st.dataframe(df)
        df.to_csv("your_attendance_data.csv", index=False)
        st.success("Attendance data downloaded successfully!")
    else:
        st.warning("No attendance data found to download.")
