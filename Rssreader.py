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

# Funktion zum Lesen der vordefinierten Suchbegriffe aus einer Datei
def load_search_terms(file_path):
    search_terms = {}
    with open(file_path, 'r') as file:
        for line in file:
            category, term = line.strip().split(':')
            if category in search_terms:
                search_terms[category].append(term)
            else:
                search_terms[category] = [term]
    return search_terms

# RSS-Feed App in Streamlit
st.title("RSS-Feed Aggregator mit Kategorien und Suchbegriffen")

# RSS Feeds aus Datei laden
rss_feed_file = 'rss_feeds.txt'  # Der Pfad zu deiner Datei mit den Feeds
rss_feeds = load_rss_feeds_from_file(rss_feed_file)

# Vordefinierte Suchbegriffe laden
search_term_file = 'searchterms.txt'  # Der Pfad zu deiner Suchbegriffsdatei
search_terms = load_search_terms(search_term_file)

# Zeige die vordefinierten Kategorien und Suchbegriffe an
st.sidebar.write("### Vordefinierte Suchbegriffe:")
for category, terms in search_terms.items():
    st.sidebar.write(f"**{category.capitalize()}**: {', '.join(terms)}")

# Benutzerdefinierte Suchbegriffe hinzufügen
new_category = st.sidebar.text_input("Neue Kategorie hinzufügen:")
new_term = st.sidebar.text_input("Neuen Suchbegriff hinzufügen:")
if st.sidebar.button("Suchbegriff hinzufügen"):
    if new_category and new_term:
        if new_category in search_terms:
            search_terms[new_category].append(new_term)
        else:
            search_terms[new_category] = [new_term]
        st.sidebar.success(f"Hinzugefügt: {new_term} unter {new_category}")
    else:
        st.sidebar.error("Bitte sowohl eine Kategorie als auch einen Suchbegriff angeben.")

# Auswahlbox zum Auswählen der RSS-Feeds
selected_feeds = st.multiselect("Wähle die RSS-Feeds, die du einbeziehen möchtest:", rss_feeds, default=rss_feeds)

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

# Überblick der Artikel als Pandas DataFrame anzeigen (jetzt am Anfang)
if articles_list:
    st.write("### Überblick der Top-Artikel")
    df = pd.DataFrame(articles_list)
    st.dataframe(df)

# Suche nach Suchbegriffen in den Artikeln
st.write("### Suche nach Artikeln basierend auf Kategorien und Suchbegriffen")
for category, terms in search_terms.items():
    st.write(f"**Kategorie: {category.capitalize()}**")
    for term in terms:
        filtered_articles = [article for article in articles_list if term.lower() in article["Title"].lower() or term.lower() in article["Summary"].lower()]
        if filtered_articles:
            st.write(f"**Suchbegriff: {term}**")
            for article in filtered_articles:
                st.write(f"- [{article['Title']}]({article['Link']}) ({article['Published']})")
        else:
            st.write(f"- Keine Artikel gefunden für: {term}")
