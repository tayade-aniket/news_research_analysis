import feedparser
from urllib.parse import quote_plus

SOURCES = {
    "Google News": "https://news.google.com/rss/search?q={}",
    "Reuters": "https://www.reuters.com/rssFeed/{}",
    "Yahoo Finance": "https://news.yahoo.com/rss/search?p={}",
    "CNBC": "https://www.cnbc.com/rss/search/?query={}"
}

def fetch_news(query: str) -> str:
    encoded_query = quote_plus(query)  # ✅ FIX HERE
    articles = []

    for source, url in SOURCES.items():
        feed_url = url.format(encoded_query)
        feed = feedparser.parse(feed_url)

        for entry in feed.entries[:3]:
            title = entry.title if hasattr(entry, "title") else ""
            articles.append(f"[{source}] {title}")

    if not articles:
        return "No relevant news articles found."

    return "\n".join(articles)
