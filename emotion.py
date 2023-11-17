import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import LabelEncoder

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
#st.sidebar.header("Upload CSV")
#uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])
uploaded_file = "emotion_data.csv"

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
