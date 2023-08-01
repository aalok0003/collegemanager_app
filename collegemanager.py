import streamlit as st

import pymongo
import bcrypt

# Connect to MongoDB Atlas
# Replace 'YOUR_CONNECTION_STRING' with your actual MongoDB Atlas connection string
client = pymongo.MongoClient('mongodb+srv://aalok:aalok@cluster0.cgn9day.mongodb.net/?retryWrites=true&w=majority')
db = client['credentials_db']  # Replace 'attendance_db' with your preferred database name
credential_collection = db['credentials_data']

# Create a session state to store user information
session_state = st.session_state.setdefault('user_info', {})

# Define session state variables
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None

# Define signup form
def signup():
    st.write("Create a new account")

    email = st.text_input("Email", key='email')
    password = st.text_input("Password", type="password", key='password')

    if st.button("Sign up"):
        # Hash the password before saving it in the database
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        # Store the user information in the database
        # Replace 'credential_collection' with your actual database collection
        credential_collection.insert_one({"email": email, "password": hashed_password})

        st.success("Account created successfully!")

# Define login form
def login():
    st.write("Kindly Login to continue.")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Log in"):
        # Check if email exists in database
        user = credential_collection.find_one({"email": email})
        if user:
            # Check if password is correct
            hashed_password = user["password"]
            if bcrypt.checkpw(password.encode("utf-8"), hashed_password):
                # Set session state variables
                st.session_state.logged_in = True
                st.session_state.current_user = user["email"]
                st.success("Logged in successfully!")
            else:
                st.error("Incorrect email or password.")
        else:
            st.error("Incorrect email or password.")

# Layout setup
st.title('College Manager')
st.write("Welcome to College Manager!")
st.write("Teachers may or may not mark your attendance seriously, but you can keep a track of it, so that you do not fall short on your attendance ever.")
st.write("Note topics, important questions, deadlines etc")

# Show Login and Signup options
option = st.radio("Select an option:", ("Login", "Sign up"))

if option == "Login":
    login()
else:
    signup()
