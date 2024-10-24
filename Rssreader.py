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

# Suchbegriffe aus einer Datei laden
search_term_file = 'searchterms.txt'  # Der Pfad zu deiner Datei mit den Suchbegriffen
search_terms = load_search_terms_from_file(search_term_file)

# Auswahlbox zum Auswählen der RSS-Feeds
selected_feeds = st.multiselect("Wähle die RSS-Feeds, die du einbeziehen möchtest:", rss_feeds, default=rss_feeds)

# Zeigt die vordefinierten Suchbegriffe aus der Datei
st.write("Vordefinierte Suchbegriffe:")
for category, terms in search_terms.items():
    st.write(f"**{category}**: {', '.join(terms)}")

# Eingabefelder zum Hinzufügen neuer Suchbegriffe
new_category = st.text_input("Neue Kategorie eingeben:")
new_term = st.text_input("Neuen Suchbegriff zur Kategorie hinzufügen:")

if st.button("Suchbegriff hinzufügen"):
    if new_category and new_term:
        if new_category in search_terms:
            search_terms[new_category].append(new_term)
        else:
            search_terms[new_category] = [new_term]
        st.success(f"Suchbegriff '{new_term}' wurde zur Kategorie '{new_category}' hinzugefügt.")

# Liste, um die Artikel für die Übersicht zu sammeln
articles_list = []

# Abrufen und Anzeigen der Feeds, die ausgewählt wurden
for feed_url in selected_feeds:
    feed = fetch_rss_feed(feed_url)

    if feed.bozo:  # Überprüfen, ob der Feed erfolgreich geparst wurde
        continue

    # Die neuesten Einträge des Feeds sammeln (z.B. die letzten 5)
    for entry in feed.entries[:5]:
        # Hinzufügen der Artikel-Daten zur Übersichtsliste
        articles_list.append({
            "Title": entry.title,
            "Published": entry.published,
            "Link": entry.link,
            "Summary": entry.summary
        })

# Überblick der Artikel als Pandas DataFrame anzeigen (am Anfang)
if articles_list:
    st.write("### Überblick der Top-Artikel")
    df = pd.DataFrame(articles_list)
    for i, row in df.iterrows():
        with st.expander(f"{row['Title']} ({row['Published']})"):
            st.write(f"**Link**: [Klicken um Artikel zu lesen]({row['Link']})")
            st.write(f"**Zusammenfassung**: {row['Summary']}")
