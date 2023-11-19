import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import LabelEncoder

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

# Function to load data from CSV
@st.cache
def load_data(uploaded_file):
    data = pd.read_csv(uploaded_file)
    return data

# Function to preprocess data
def preprocess_data(df):
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['Date'] = df['Timestamp'].dt.date
    df['Time'] = df['Timestamp'].dt.time

    # Encode emotions using LabelEncoder
    label_encoder = LabelEncoder()
    df['Emotion_Encoded'] = label_encoder.fit_transform(df['Emotion'])

    return df, label_encoder

# Streamlit app
def main():
    # Check if user is logged in
    if 'is_logged_in' not in st.session_state:
        st.session_state['is_logged_in'] = False
        st.session_state['username'] = None

    # Display login page if not logged in
    if not st.session_state['is_logged_in']:
        st.title("<b>Domestic Emotion Monitoring System</b>")

        # Input fields for username and password
        username = st.text_input("Username:")
        password = st.text_input("Password:", type="password")

        # Login button
        if st.button("Login"):
            if authenticate(username, password):
                st.session_state['is_logged_in'] = True
                st.session_state['username'] = username
                st.experimental_rerun()
            else:
                st.error("Invalid username or password. Please try again.")

    # Display main content if logged in
    else:
        st.success(f"Welcome, {st.session_state['username']}!")

        # Sidebar for file selection
        uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

        # Display data
        if uploaded_file is not None:
            df, label_encoder = preprocess_data(load_data(uploaded_file))

            # Display raw data
            st.subheader("Preprocessed Data")
            st.write(df)

            # User input for timestamp range
            try:
                start_timestamp = pd.to_datetime(st.sidebar.text_input("Select Start Timestamp (YYYY-MM-DD HH:MM:SS)", df['Timestamp'].iloc[0]))
                end_timestamp = pd.to_datetime(st.sidebar.text_input("Select End Timestamp (YYYY-MM-DD HH:MM:SS)", df['Timestamp'].iloc[-1]))
            except ValueError:
                st.error("Invalid timestamp format. Please enter timestamps in the format: YYYY-MM-DD HH:MM:SS")
                return

            # Filter data for the selected period
            selected_data = df[(df['Timestamp'] >= start_timestamp) & (df['Timestamp'] <= end_timestamp)]

            # Display emotions count for the selected period
            if not selected_data.empty:
                st.subheader(f"Emotion Counts for Period {start_timestamp} to {end_timestamp}")
                filtered_counts = selected_data.groupby('Emotion')['Timestamp'].count().reset_index(name='Count')
                fig = px.bar(filtered_counts, x='Emotion', y='Count', color='Emotion', title='Emotion Counts for the Selected Period')
                st.plotly_chart(fig)
            else:
                st.warning("No data available for the selected period.")

        else:
            st.info("Please upload a CSV file.")

        # Logout option
        if st.button("Logout"):
            clear_session_state()
            st.experimental_rerun()

        # Add footnote to all pages
        st.markdown("<p style='text-align: center;'>This project is supported by All India Council for Technical Education (AICTE), Ministry of Education, India, Arm Education, and STMicroelectronics.<br>Developers: Charan Velavan, Ebi Manuel, Benie Jaison A T, and Akshay B<br>Mentor: M.Lingeshwaran<br>St. Joseph's College of Engineering, OMR, Chennai -119.</p>", unsafe_allow_html=True)

# Run the app
if __name__ == '__main__':
    main()
