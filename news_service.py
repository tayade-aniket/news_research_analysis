import feedparser

def fetch_news(query):
    url = f"https://news.google.com/rss/search?q={query}"
    feed = feedparser.parse(url)

    articles = []
    for entry in feed.entries[:10]:
        articles.append(f"- {entry.title}")

    return "\n".join(articles)
