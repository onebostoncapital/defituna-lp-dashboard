import feedparser


def fetch_crypto_news():
    """
    Fetch crypto-related news and return a normalized FA signal.
    """

    feeds = [
        "https://cointelegraph.com/rss",
        "https://www.coindesk.com/arc/outboundfeeds/rss/"
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
            score += 0.05  # small positive bias per item

    return {
        "score": round(score, 3),
        "items": items
    }
