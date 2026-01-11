import feedparser


def fetch_macro_news():
    """
    Fetch macro-economic news and return a normalized FA signal.
    """

    feeds = [
        "https://www.reuters.com/rssFeed/worldNews",
        "https://www.investing.com/rss/news_285.rss"
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
            score -= 0.03  # macro news adds slight risk bias

    return {
        "score": round(score, 3),
        "items": items
    }
