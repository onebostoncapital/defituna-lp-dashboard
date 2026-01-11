import feedparser


def fetch_geopolitical_news():
    """
    Fetch geopolitical news and return a normalized FA signal.
    """

    feeds = [
        "https://www.reuters.com/rssFeed/worldNews",
        "https://feeds.bbci.co.uk/news/world/rss.xml"
    ]

    items = []
    score = 0.0

    for url in feeds:
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:
            items.append({
                "title": entry.get("title", ""),
                "link": entry.get("link", "")
            })
            score -= 0.04  # geopolitical risk bias

    return {
        "score": round(score, 3),
        "items": items
    }
