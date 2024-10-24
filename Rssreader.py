import feedparser
import streamlit as st
import pandas as pd

# Funktion zum Lesen der RSS-Feeds aus einer Datei
def load_rss_feeds_from_file(file_path):
    with open(file_path, 'r') as file:
        rss_feeds = [line.strip() for line in file.readlines() if line.strip()]
    return rss_feeds

# Funktion zum Lesen von Suchbegriffen aus einer Datei
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

# Funktion zum Abrufen und Bündeln der Feeds
def fetch_rss_feed(url):
    return feedparser.parse(url)

# Streamlit Anwendung
st.title("RSS-Feed Aggregator mit Suchbegriffen")

# RSS Feeds aus einer Datei laden
rss_feed_file = 'rss_feeds.txt'  # Der Pfad zu deiner Datei mit den Feeds
rss_feeds = load_rss_feeds_from_file(rss_feed_file)

# Auswahlbox zum Auswählen der RSS-Feeds
selected_feeds = st.multiselect("Wähle die RSS-Feeds, die du einbeziehen möchtest:", rss_feeds, default=rss_feeds)

# Optional: Eingabefeld für zusätzliche Feeds
new_feed_url = st.text_input("Füge einen neuen RSS-Feed hinzu:")

if new_feed_url:
    selected_feeds.append(new_feed_url)

# Suchbegriffe aus einer Datei laden
search_terms_file = 'searchterms.txt'  # Pfad zu deiner Datei mit den Suchbegriffen
search_terms = load_search_terms_from_file(search_terms_file)

# Auswahl der Suchbegriffe nach Kategorien (alle Suchbegriffe vorausgewählt)
selected_terms = []
#for category, terms in search_terms.items():
#   selected = st.multiselect(f"Wähle Suchbegriffe aus der Kategorie '{category}':", terms, default=terms)
#    selected_terms.extend(selected)

# Liste, um die Artikel für die Übersicht zu sammeln
articles_list = []

# Abrufen und Anzeigen der Feeds, die ausgewählt wurden
for feed_url in selected_feeds:
    feed = fetch_rss_feed(feed_url)

    if feed.bozo:  # Überprüfen, ob der Feed erfolgreich geparst wurde
        continue

    # Die neuesten Einträge des Feeds sammeln (z.B. die letzten 5)
    for entry in feed.entries[:5]:
        # Filter auf Basis der Suchbegriffe anwenden
        if any(term.lower() in entry.title.lower() or term.lower() in entry.summary.lower() for term in selected_terms):
            # Hinzufügen der Artikel-Daten zur Übersichtsliste
            articles_list.append({
                "Title": entry.title,
                "Published": entry.published,
                "Link": entry.link,
                "Summary": entry.summary
            })

# Überblick der Artikel als Pandas DataFrame anzeigen (jetzt am Anfang)
if articles_list:
    st.write("### Überblick der Top-Artikel (basierend auf den ausgewählten Suchbegriffen)")
    df = pd.DataFrame(articles_list)
    st.dataframe(df)

# Details zu jedem Artikel anzeigen (mit Click-to-Expand)
for article in articles_list:
    with st.expander(f"{article['Title']} (Published: {article['Published']})"):
        st.write(article['Summary'])
        st.write(f"[Mehr lesen]({article['Link']})")
