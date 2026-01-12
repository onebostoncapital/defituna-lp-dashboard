import feedparser
import time

# ---------------------------------------
# CONFIG
# ---------------------------------------
NEWS_REFRESH_SECONDS = 15 * 60  # 15 minutes

CRYPTO_RSS_FEEDS = [
    "https://cointelegraph.com/rss",
    "https://cryptonews.com/news/feed/",
    "https://www.coindesk.com/arc/outboundfeeds/rss/"
]

# ---------------------------------------
# IN-MEMORY CACHE
# ---------------------------------------
_cache = {
    "timestamp": 0,
    "data": None
}


# ---------------------------------------
# PUBLIC API
# ---------------------------------------
def fetch_crypto_news():
    """
    Returns:
    {
        "score": float,
        "drivers": [string],
        "items": [
            {"title": str, "link": str}
        ]
    }
    """

    now = time.time()

    # -----------------------------
    # CACHE CHECK
    # -----------------------------
    if (
        _cache["data"] is not None
        and (now - _cache["timestamp"]) < NEWS_REFRESH_SECONDS
    ):
        return _cache["data"]

    items = []
    drivers = []
    score = 0.0

    # -----------------------------
    # FETCH RSS FEEDS
    # -----------------------------
    for feed_url in CRYPTO_RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)

            for entry in feed.entries[:3]:
                title = entry.get("title", "").strip()
                link = entry.get("link", "").strip()

                if not title or not link:
                    continue

                items.append({
                    "title": title,
                    "link": link
                })

        except Exception:
            continue

    # -----------------------------
    # SCORING LOGIC (LIGHTWEIGHT)
    # -----------------------------
    if items:
        score = 0.3
        drivers.append("Recent crypto market news activity detected")

    result = {
        "score": score,
        "drivers": drivers,
        "items": items
    }

    # -----------------------------
    # CACHE SAVE
    # -----------------------------
    _cache["data"] = result
    _cache["timestamp"] = now

    return result
