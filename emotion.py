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

# Streamlit app
def main():
    st.title("Login Page")

    # Input fields for username and password
    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")

    # Login button
    if st.button("Login"):
        if authenticate(username, password):
            st.success(f"Welcome, {username}!")

            # Clear the input fields after successful login
            st.text_input("Username:", value="")
            st.text_input("Password:", value="", type="password")

            # Load the CSV file
            @st.cache_data
            def load_data(file_path):
                data = pd.read_csv(file_path)
                return data

            # Preprocess the data
            def preprocess_data(df):
                df['Timestamp'] = pd.to_datetime(df['Timestamp'])
                df['Date'] = df['Timestamp'].dt.date
                df['Time'] = df['Timestamp'].dt.time

                # Encode emotions using LabelEncoder
                label_encoder = LabelEncoder()
                df['Emotion_Encoded'] = label_encoder.fit_transform(df['Emotion'])

                return df, label_encoder

            # Sidebar for file selection
            uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])

            # Display data
            if uploaded_file is not None:
                df, label_encoder = preprocess_data(load_data(uploaded_file))

                # Display raw data
                st.subheader("Preprocessed Data")
                st.write(df)

                # User input for timestamp range
                start_timestamp = st.sidebar.text_input("Select Start Timestamp(YYYY-MM-DD HH:MM:SS)", df['Timestamp'].iloc[0])
                end_timestamp = st.sidebar.text_input("Select End Timestamp(YYYY-MM-DD HH:MM:SS)", df['Timestamp'].iloc[-1])

                # Filter data for the selected period
                selected_data = df[(df['Timestamp'] >= pd.to_datetime(start_timestamp)) & (df['Timestamp'] <= pd.to_datetime(end_timestamp))]

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
        else:
            st.error("Invalid username or password. Please try again.")

if __name__ == '__main__':
    main()
