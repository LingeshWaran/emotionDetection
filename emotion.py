# Filename: cyberspartans.py
import streamlit as st

# Initialize session state
if 'is_logged_in' not in st.session_state:
    st.session_state['is_logged_in'] = False
    st.session_state['username'] = None

# Define a dictionary to store user credentials
user_credentials = {
    'user1': 'password1',
    'user2': 'password2',
    # Add more usernames and passwords as needed
}

# Function to check if the entered credentials are valid
def authenticate(username, password):
    stored_password = user_credentials.get(username)
    if stored_password is not None and stored_password == password:
        return True
    return False

# Function to clear sensitive information from the session state
def clear_session_state():
    st.session_state['is_logged_in'] = False
    st.session_state['username'] = None

# Function to display videos and blinking button
def display_videos():
    # Video 1 - Original Video
    st.subheader("Title: Original Video")
    v1_url = "v1.mp4"  # Assuming v1.mp4 is in the same directory
    st.video(v1_url, start_time=0)

    # Video 2 - Annotated Video
    st.subheader("Title: Annotated Video")
    v2_url = "v2.mp4"  # Assuming v2.mp4 is in the same directory
    st.video(v2_url, start_time=0)

    # Blinking red button
    blink_text = st.markdown('<button style="background-color: red; color: black;">Alert!</button>', unsafe_allow_html=True)
    # Blinking functionality (Note: Blinking might not work in some environments)
    st.experimental_rerun()

# Streamlit app
def main():
    # Add a footnote to all pages
    st.markdown("<p style='text-align: center;'>Problem Statement ID:1416<br>Problem Statement Title: AI based Automatic alarm generation and dropping of payload at a particular object through a Drone.<br>Organization: Ministry of Defence<br>Grand finale of Smart India Hackathon 2023 - Software Edition.<br>This project is supported by Ministry of Defence and Ministry of Education, Government of India.<br>Domain Bucket: Disaster Management<br>Team Name: Cyber Spartans<br>Team Leader: Charan<br> Team Members: Akshay B, Alfred D, Tejaswin S, Prakriti Harith, and Thanisqka N<br>Mentor: M. Lingeshwaran<br>St. Joseph's College of Engineering, OMR, Chennai -119.</p>", unsafe_allow_html=True)

    # Title
    st.title("AI based Automatic alarm generation and dropping of payload at a particular object through a Drone")

    # Display the login page if not logged in
    if not st.session_state['is_logged_in']:
        # Input fields for username and password
        username = st.text_input("Username:")
        password = st.text_input("Password:", type="password")

        # Login button
        if st.button("Login"):
            if authenticate(username, password):
                st.session_state['is_logged_in'] = True
                st.session_state['username'] = username

    # Display main content if logged in
    if st.session_state['is_logged_in']:
        st.success(f"Welcome, {st.session_state['username']}!")

        # Logout option
        if st.button("Logout"):
            clear_session_state()

        # Display videos and blinking button
        display_videos()

# Run the app
if __name__ == '__main__':
    main()
