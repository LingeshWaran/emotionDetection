import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit.hashing import generate_password_hash, verify_password
from st_aggrid import AgGrid

# Replace these credentials with your own
USERNAME = 'your_username'
PASSWORD_HASH = generate_password_hash('your_password')

# Flag to check if the user is logged in
logged_in = False

@st.cache
def read_data():
    # Read CSV file
    df = pd.read_csv('emotion_data.csv')
    return df

def login():
    global logged_in
    if st.button("Login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if username == USERNAME and verify_password(password, PASSWORD_HASH):
            logged_in = True
            st.success("Logged in successfully!")

    return logged_in

def create_line_graph(df):
    fig = px.line(df, x='Timestamp', y='Emotion', markers=True, title='Emotion vs Timestamp')
    return fig

def create_bar_graph(df):
    fig = px.bar(df['Emotion'].value_counts().reset_index(), x='index', y='Emotion', title='Emotion Counts vs Timestamp',
                 labels={'index': 'Emotion', 'Emotion': 'Count'})
    dominant_emotion = df['Emotion'].value_counts().idxmax()
    return fig, dominant_emotion

def main():
    global logged_in
    st.title("Emotion Analysis App")

    if not logged_in:
        logged_in = login()

    if logged_in:
        df = read_data()

        # Create line graph
        line_graph = create_line_graph(df)

        # Create bar graph
        bar_graph, dominant_emotion = create_bar_graph(df)

        # Display graphs
        st.markdown("## Emotion vs Timestamp")
        st.plotly_chart(line_graph, use_container_width=True)

        st.markdown("## Emotion Counts vs Timestamp")
        st.plotly_chart(bar_graph, use_container_width=True)

        st.markdown(f"**Dominant Emotion:** {dominant_emotion}")

        # Display AgGrid table
        st.markdown("## Emotion Data Table")
        AgGrid(df)

if __name__ == "__main__":
    main()
