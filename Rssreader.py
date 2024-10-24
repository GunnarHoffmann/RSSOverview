import openai
import feedparser
import streamlit as st

# Read the OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["openai"]["api_key"]

# Function to call OpenAI's GPT API to summarize the content
def summarize_content_with_gpt(content):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # You can use other models like 'gpt-3.5-turbo' as well
            prompt=f"Summarize the following content:\n\n{content}",
            max_tokens=150,  # Adjust for the length of the summary
            temperature=0.7  # Adjust to control the creativity
        )
        summary = response.choices[0].text.strip()
        return summary
    except Exception as e:
        return f"Error summarizing content: {e}"

# Function to read RSS feeds from a file
def load_rss_feeds_from_file(file_path):
    with open(file_path, 'r') as file:
        rss_feeds = [line.strip() for line in file.readlines() if line.strip()]
    return rss_feeds

# Function to fetch and parse the feeds
def fetch_rss_feed(url):
    return feedparser.parse(url)

# Apply custom CSS for background colors
st.markdown("""
    <style>
    .rss-section {
        background-color: #f0f0f0;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .combined-section {
