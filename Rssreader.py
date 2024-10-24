import feedparser
import streamlit as st

# Liste von RSS-Feed-URLs
rss_feeds = [
    'https://kiupdate.podigee.io/feed/mp3',                     # Beispiel: TechCrunch
    'https://www.heise.de/rss/heise-atom.xml',                      # Beispiel: Heise
]

# Funktion zum Abrufen und Bündeln der Feeds
def fetch_rss_feed(url):
    return feedparser.parse(url)

# Streamlit Anwendung
st.title("RSS-Feed Aggregator")

# Eingabefeld für zusätzliche Feeds
new_feed_url = st.text_input("Füge einen neuen RSS-Feed hinzu:")

if new_feed_url:
    rss_feeds.append(new_feed_url)

st.write(f"Es werden {len(rss_feeds)} Feeds abgerufen.")

# Abrufen und Anzeigen der Feeds
for feed_url in rss_feeds:
    st.write(f"**RSS-Feed von:** {feed_url}")
    feed = fetch_rss_feed(feed_url)

    if feed.bozo:  # Überprüfen, ob der Feed erfolgreich geparst wurde
        st.error(f"Fehler beim Abrufen des Feeds: {feed_url}")
        continue

    st.write(f"**Feed-Titel:** {feed.feed.title}")
    
    # Die neuesten Einträge des Feeds anzeigen (z.B. die letzten 5)
    for entry in feed.entries[:5]:
        st.subheader(entry.title)
        st.write(entry.published)
        st.write(entry.link)
        st.write(entry.summary)
        st.write("---")
