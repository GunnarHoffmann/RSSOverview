import feedparser
import streamlit as st
import pandas as pd

# Funktion zum Lesen der RSS-Feeds aus einer Datei
def load_rss_feeds_from_file(file_path):
    with open(file_path, 'r') as file:
        rss_feeds = [line.strip() for line in file.readlines() if line.strip()]
    return rss_feeds


# Funktion zum Abrufen und Bündeln der Feeds
def fetch_rss_feed(url):
    return feedparser.parse(url)

# Streamlit Anwendung
st.title("RSS-Feed Aggregator")

# RSS Feeds aus einer Datei laden
rss_feed_file = 'rss_feeds.txt'  
# Der Pfad zu deiner Datei mit den Feeds
rss_feeds = load_rss_feeds_from_file(rss_feed_file)

# Auswahlbox zum Auswählen der RSS-Feeds
selected_feeds = st.multiselect("Wähle die RSS-Feeds, die du einbeziehen möchtest:", rss_feeds, default=rss_feeds)


# Liste, um die Artikel für die Übersicht zu sammeln
articles_list = []

# Abrufen und Anzeigen der Feeds
for feed_url in rss_feeds:
    feed = fetch_rss_feed(feed_url)

    if feed.bozo:  # Überprüfen, ob der Feed erfolgreich geparst wurde
        continue

    # Die neuesten Einträge des Feeds sammeln (z.B. die letzten 5)
    for entry in feed.entries[:5]:
        # Hinzufügen der Artikel-Daten zur Übersichtsliste
        articles_list.append({
            "Title": entry.title,
            "Published": entry.published,
            "Link": entry.link
        })

# Überblick der Artikel als Pandas DataFrame anzeigen (jetzt am Anfang)
if articles_list:
    st.write("### Überblick der Top-Artikel")
    df = pd.DataFrame(articles_list)
    st.dataframe(df)

# Abrufen und Anzeigen der Feeds im Detail (jetzt nach dem Überblick)
st.write(f"Es werden {len(rss_feeds)} Feeds abgerufen.")
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
