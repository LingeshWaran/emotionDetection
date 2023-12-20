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
@st.cache(allow_output_mutation=True)
def load_data():
    # Assuming "emotion_data.csv" is in the root of the Git repo
    data = pd.read_csv("emotion_data.csv")
    return data

# Function to preprocess data
def preprocess_data(df):
    df = df.copy()  # Clone the DataFrame to avoid mutability issues
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])  # Convert the 'Timestamp' column to Timestamp objects
    df['Date'] = df['Timestamp'].dt.date
    df['Time'] = df['Timestamp'].dt.time

    # Encode emotions using LabelEncoder
    label_encoder = LabelEncoder()
    df['Emotion_Encoded'] = label_encoder.fit_transform(df['Emotion'])

    return df, label_encoder

# Function to plot emotions over time
def plot_emotions_over_time(df):
    # Group data by Timestamp and Emotion to get counts
    emotions_over_time = df.groupby(['Timestamp', 'Emotion']).size().reset_index(name='Count')

    # Plotting emotions over time
    fig = px.line(emotions_over_time, x='Timestamp', y='Count', color='Emotion', title='Emotions Over Time')
    st.plotly_chart(fig)

    # Identify the dominant emotion
    dominant_emotion = df['Emotion'].mode().values[0]
    st.write(f"Dominant Emotion: {dominant_emotion}")

# Function to plot emotions against timestamps
def plot_emotions_vs_timestamp(df):
    # Plot emotions against timestamps
    fig = px.scatter(df, x='Timestamp', y='Emotion_Encoded', color='Emotion', title='Emotions vs Timestamp')
    st.plotly_chart(fig)

# Streamlit app
def main():
    # Check if the user is logged in
    if 'is_logged_in' not in st.session_state:
        st.session_state['is_logged_in'] = False
        st.session_state['username'] = None

    # Display the login page if not logged in
    if not st.session_state['is_logged_in']:
        st.title("Domestic Emotion Monitoring System")

        # Input fields for username and password
        username = st.text_input("Username:")
        password = st.text_input("Password:", type="password")

        # Login button
        if st.button("Login"):
            if authenticate(username, password):
                st.session_state['is_logged_in'] = True
                st.session_state['username'] = username
                st.rerun()
            else:
                st.error("Invalid username or password. Please try again.")

        # Add a footnote to the login page
        st.markdown("<p style='text-align: center;'>This project is supported by All India Council for Technical Education (AICTE), Ministry of Education, India, Arm Education, and STMicroelectronics.<br>Developers: Charan Velavan, Ebi Manuel, Benie Jaison A T, and Akshay B<br>Mentor: M. Lingeshwaran<br>St. Joseph's College of Engineering, OMR, Chennai -119.</p>", unsafe_allow_html=True)

    # Display main content if logged in
    else:
        st.success(f"Welcome, {st.session_state['username']}!")

        # Load the CSV file
        df = load_data()

        # Preprocess the data
        df, label_encoder = preprocess_data(df)

        # Display raw data
        st.subheader("Preprocessed Data")
        st.write(df)

        # User input for the timestamp range
        start_timestamp_str = st.sidebar.text_input("Select Start Timestamp (YYYY-MM-DD HH:MM:SS)", str(df['Timestamp'].iloc[0]))
        end_timestamp_str = st.sidebar.text_input("Select End Timestamp (YYYY-MM-DD HH:MM:SS)", str(df['Timestamp'].iloc[-1]))

        try:
            start_timestamp = pd.to_datetime(start_timestamp_str)
            end_timestamp = pd.to_datetime(end_timestamp_str)
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

        # Display line graph of emotions over time and identify dominant emotion
        st.subheader("Emotions Over Time")
        plot_emotions_over_time(selected_data)

        # Display emotions vs timestamp graph
        st.subheader("Emotions vs Timestamp")
        plot_emotions_vs_timestamp(selected_data)

        # Logout option
        if st.button("Logout"):
            clear_session_state()
            st.rerun()

        # Add a footnote to all pages
        st.markdown("<p style='text-align: center;'>This project is supported by All India Council for Technical Education (AICTE), Ministry of Education, India, Arm Education, and STMicroelectronics.<br>Developers: Charan Velavan, Ebi Manuel, Benie Jaison A T, and Akshay B<br>Mentor: M. Lingeshwaran<br>St. Joseph's College of Engineering, OMR, Chennai -119.</p>", unsafe_allow_html=True)

# Run the app
if _name_ == '_main_':
    main()
