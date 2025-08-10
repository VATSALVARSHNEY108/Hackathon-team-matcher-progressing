author = "Vatsal Vasrhney"

import random
import streamlit as st
from csv_writer import write_participants_to_csv
from generate import generate_ideas
from webscraper import scrape_hackathon_page
import hashlib
import os


# Function to read the previous hash from a file
def read_previous_hash(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return file.read().strip()
    return None


# Sidebar for user input
st.sidebar.header("Enter your details")
hackathon_link = st.sidebar.text_input(
    "Hackathon Link",
    value="https://ai-devsummit-2024-hackathon.devpost.com/"
)
devpost_username = st.sidebar.text_input(
    "Devpost Username",
    value="gclark0812@gmail.com"
)
devpost_password = st.sidebar.text_input(
    "Devpost Password",
    type="password",
    value="SecurePrivatePassword"
)

hackathon_description = st.sidebar.text_area(
    "Hackathon Description",
    height=200,
    value="""<YOUR HACKATHON DESCRIPTION HERE>"""
)
hackathon_sponsors = st.sidebar.text_input(
    "Hackathon Sponsors (comma separated, no spaces)",
    value="AWS,LaunchDarkly,GitHub,Convex"
)

# Main panel
st.title("Hackathon Team Finder")
st.subheader("By Boopesh S., Walter T., And Griffin C.")

# Submit button
if st.sidebar.button("Submit"):
    if hackathon_link:
        # Calculate the hash of the current hackathon link
        current_hash = hashlib.md5(hackathon_link.encode()).hexdigest()
        previous_hash = read_previous_hash('../../hackathon team finder/previous_hash.txt')

        # Check if the hackathon link has changed
        if current_hash != previous_hash:
            participants = scrape_hackathon_page(hackathon_link, devpost_username, devpost_password)
            if participants:
                st.write(f"Scraped {len(participants)} participants.")
                write_participants_to_csv(participants, filename=f"{current_hash}.csv")
                st.write("Data written to participants.csv.")
            else:
                st.write("Failed to scrape participants.")
        else:
            st.write("Hackathon link has not changed. No need to scrape again.")

        st.write("Generating ideas...")
        content = generate_ideas(hackathon_description, hackathon_sponsors)
        st.write(content)
    else:
        st.write("Please enter a hackathon link.")

# ----------------------
# Local Feature Flag Mock
# ----------------------
feature_key = "show_resume_feature"
user = {
    "key": random.randint(1, 10000),  # User ID
    "name": devpost_username
}

# Manually set this for local testing
resume_feature_enabled = True  # Change to False to disable

st.write("User Info:", user)
st.write(f"{feature_key}: {resume_feature_enabled}")
