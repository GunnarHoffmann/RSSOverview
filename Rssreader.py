import feedparser
import streamlit as st

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

# Function to fetch and parse the feeds
def fetch_rss_feed(url):
    return feedparser.parse(url)

# Streamlit application
st.title("Data & AI Newsfeed")
st.subheader("Aggregating curated RSS feeds and Internet-based semantic search in one place")

# ----------- RSS Feeds Section ------------
st.header("RSS Feeds")

# Load RSS feeds from a file
rss_feed_file = 'rss_feeds.txt'  # Path to your file with RSS feeds
rss_feeds = load_rss_feeds_from_file(rss_feed_file)

# Multi-select box for choosing RSS feeds
selected_feeds = st.multiselect("Select the RSS feeds you'd like to include:", rss_feeds, default=rss_feeds)

# List to collect articles for display
articles_list = []

# Fetch and display the selected feeds
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

# Display details for each article (with Click-to-Expand functionality)
for article in articles_list:
    with st.expander(f"{article['Title']} (Published: {article['Published']})"):
        st.write(article['Summary'])
        st.write(f"[Read more]({article['Link']})")

# Add visual separation between sections
st.markdown("---")  # Horizontal line

# ----------- Internet-based Semantic Search Section ------------
st.header("Internet-based Semantic Search")

# Load search terms from a file
search_terms_file = 'searchterms.txt'  # Path to your file with search terms
search_terms = load_search_terms_from_file(search_terms_file)

# Multi-select box for selecting search terms by category (pre-selecting all terms)
selected_terms = []
for category, terms in search_terms.items():
    selected = st.multiselect(f"Select search terms from the '{category}' category:", terms, default=terms)
    selected_terms.extend(selected)
