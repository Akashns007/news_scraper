import streamlit as st
import json
import os
from run_spider import run_spider

def load_news():
    if os.path.exists("latest_news.json"):
        with open("latest_news.json") as f:
            return json.load(f)
    return []

st.set_page_config(page_title="News App", page_icon="📰")

st.title("News App")
st.sidebar.header("Navigation")
page = st.sidebar.selectbox("Go to", ["Home", "Get News"])

if page == "Home":
    st.header("Welcome to the News App")
    st.write("All the news at the tip of your hands ✨.")
    # Add image to the home page
    # st.image("home.jpeg")
    
elif page == "Get News":
    st.header("Get the Latest News")
    if st.button("Fetch News"):
        run_spider()
        st.success("News fetched successfully!")

    news_data = load_news()
    if news_data:
        for item in reversed(news_data):
            st.write(f"**{item['headline']}**")
            st.write(f"[Read more]({item['news_link']})")
            st.write("---")
    else:
        st.write("No news to display. Click the button above to fetch news.")

# To run the Streamlit app, use the command:
# streamlit run app.py
