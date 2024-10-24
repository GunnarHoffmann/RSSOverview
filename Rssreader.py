import os
import requests
import json
import feedparser
import streamlit as st

# Read the Azure OpenAI API details from Streamlit secrets
api_key = st.secrets["azure_openai"]["api_key"]
endpoint = st.secrets["azure_openai"]["endpoint"]
deployment_name = st.secrets["azure_openai"]["deployment_name"]

# Function to call Azure OpenAI's Chat API to summarize the content
def summarize_content_with_azure(content):
    try:
        headers = {
            "Content-Type": "application/json",
            "api-key": api_key
        }
        body = {
            "messages": [
                {"role": "user", "content": f"Summarize the following content:\n\n{content}"}
            ]
        }
        response = requests.post(
            f"{endpoint}/openai/deployments/{deployment_name}/chat/completions?api-version=2023-03-15-preview",
            headers=headers,
            json=body
        )
        response.raise_for_status()
        data = response.json()
        summary = data["choices"][0]["message"]["content"].strip()
        return summary
    except Exception as e:
        return f"Error summarizing content: {e}"

# Function to read RSS feeds from a file
def load_rss_feeds_from_file(file_path):
    with open(file_path, 'r') as file:
        rss_feeds = [line.strip() for line in file.readlines() if line.strip()]
    return rss_feeds

# Function to read search terms from a file
def load_search_terms_from_file(file_path):
    search_terms = {}
    with open(file_path, 'r') as file:
        for line in file:
            if ':' in line:
                category, term = line.strip().split(':')
                if category in search_terms:
                    search_terms[category].append(term)
                else:
                    search_terms[category] = [term]
    return search_terms

# Function to fetch and parse the RSS feeds
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
    .search-section {
        background-color: #f0f0f0;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .combined-section {
        background-color: #e0e0e0;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Streamlit application
st.title("Data & AI Newsfeed")
st.subheader("Aggregating curated RSS feeds and Internet-based semantic search in one place")

# Initialize session state for toggle logic
if 'show_rss_output' not in st.session_state:
    st.session_state['show_rss_output'] = False

if 'show_search_output' not in st.session_state:
    st.session_state['show_search_output'] = False

if 'show_combined_output' not in st.session_state:
    st.session_state['show_combined_output'] = False

# Function to toggle RSS output visibility
def toggle_rss_output():
    st.session_state['show_rss_output'] = not st.session_state['show_rss_output']

# Function to toggle search output visibility
def toggle_search_output():
    st.session_state['show_search_output'] = not st.session_state['show_search_output']

# Function to toggle combined output visibility
def toggle_combined_output():
    st.session_state['show_combined_output'] = not st.session_state['show_combined_output']

# ----------- RSS Feeds Section (Form with Background) ------------
with st.form(key='rss_form'):
    st.markdown('<div class="rss-section">', unsafe_allow_html=True)
    
    st.header("RSS Feeds")

    # Load RSS feeds from a file
    rss_feed_file = 'rss_feeds.txt'  # Path to your file with RSS feeds
    rss_feeds = load_rss_feeds_from_file(rss_feed_file)

    # Multi-select box for choosing RSS feeds
    selected_feeds = st.multiselect("Select the RSS feeds you'd like to include:", rss_feeds, default=rss_feeds)

    # List to collect articles for display
    articles_list = []
    combined_rss_content = ""

    # Always load RSS feed content for Combined Output
    for feed_url in selected_feeds:
        feed = fetch_rss_feed(feed_url)

        if feed.bozo:  # Check if the feed was parsed successfully
            continue

        # Collect the latest entries from the feed (e.g., the last 5)
        for entry in feed.entries[:5]:
            articles_list.append({
                "Title": entry.title,
                "Published": entry.published,
                "Link": entry.link,
                "Summary": entry.summary
            })
            combined_rss_content += f"{entry.title}\n{entry.published}\n{entry.summary}\n\n"

    # Submit button to toggle RSS output
    rss_submit = st.form_submit_button(label="Show/Hide RSS Output", on_click=toggle_rss_output)

    # Toggle logic to show or hide the RSS output
    if st.session_state['show_rss_output'] and rss_submit:
        for article in articles_list:
            with st.expander(f"{article['Title']} (Published: {article['Published']})"):
                st.write(article['Summary'])
                st.write(f"[Read more]({article['Link']})")

    st.markdown('</div>', unsafe_allow_html=True)

# Add visual separation between sections
st.markdown("---")  # Horizontal line

# ----------- Internet-based Semantic Search Section (Form with Background) ------------
with st.form(key='search_form'):
    st.markdown('<div class="search-section">', unsafe_allow_html=True)
    
    st.header("Internet-based Semantic Search")

    # Load search terms from a file
    search_terms_file = 'searchterms.txt'  # Path to your file with search terms
    search_terms = load_search_terms_from_file(search_terms_file)

    # Multi-select box for selecting search terms by category (pre-selecting all terms)
    selected_terms = []
    for category, terms in search_terms.items():
        selected = st.multiselect(f"Select search terms from the '{category}' category:", terms, default=terms)
        selected_terms.extend(selected)

    # Submit button for search terms form
    search_submit = st.form_submit_button(label="Show/Hide Search Output", on_click=toggle_search_output)

    # Handle form submission for search terms (control visibility with toggle)
    if st.session_state['show_search_output'] and search_submit:
        st.write("Selected search terms:", ", ".join(selected_terms))

    st.markdown('</div>', unsafe_allow_html=True)

# ----------- Combined Output Section (Form with Background) ------------
with st.form(key='combined_output_form'):
    st.markdown('<div class="combined-section">', unsafe_allow_html=True)
    
    st.header("Combined Output")

    # Submit button to toggle Combined Output visibility
    combined_submit = st.form_submit_button(label="Show/Hide Combined Output", on_click=toggle_combined_output)

    # Display combined RSS feed content in a text area (controlled by toggle)
    if st.session_state['show_combined_output'] and combined_submit:
        if articles_list:
            st.text_area("Combined RSS Feed Content", value=combined_rss_content, height=300)

            # Summarize the content using Azure OpenAI
            summary = summarize_content_with_azure(combined_rss_content)
            st.subheader("Summary (Powered by Azure OpenAI):")
            st.write(summary)

    st.markdown('</div>', unsafe_allow_html=True)
