import feedparser
from datetime import datetime


CRYPTO_RSS_FEEDS = {
    "CoinDesk": "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "CoinTelegraph": "https://cointelegraph.com/rss",
    "Decrypt": "https://decrypt.co/feed"
}


NEGATIVE_KEYWORDS = [
    "hack", "exploit", "outage", "downtime", "lawsuit",
    "ban", "crash", "halt", "breach", "liquidation"
]

POSITIVE_KEYWORDS = [
    "approval", "partnership", "upgrade", "launch",
    "adoption", "etf", "integration", "growth"
]


def score_headline(headline: str):
    """
    Score a crypto news headline for LP risk relevance.
    """

    headline_lower = headline.lower()

    negative_hits = sum(word in headline_lower for word in NEGATIVE_KEYWORDS)
    positive_hits = sum(word in headline_lower for word in POSITIVE_KEYWORDS)

    if negative_hits > positive_hits and negative_hits > 0:
        impact = "Negative"
        score = -20 - (negative_hits * 2)
    elif positive_hits > negative_hits and positive_hits > 0:
        impact = "Positive"
        score = 15 + (positive_hits * 2)
    else:
        impact = "Neutral"
        score = 0

    score = max(min(score, 30), -30)

    confidence = min((abs(score) / 30), 1.0)

    return impact, score, round(confidence, 2)


def fetch_crypto_news(limit_per_source: int = 5):
    """
    Fetch and score crypto news from multiple RSS sources.

    Output:
        List of dicts with headline, source, impact, score, confidence, timestamp
    """

    news_items = []

    for source, url in CRYPTO_RSS_FEEDS.items():
        try:
            feed = feedparser.parse(url)

            for entry in feed.entries[:limit_per_source]:
                headline = entry.title
                published = entry.get("published", None)

                impact, score, confidence = score_headline(headline)

                news_items.append({
                    "headline": headline,
                    "source": source,
                    "impact": impact,
                    "score": score,
                    "confidence": confidence,
                    "timestamp": published or datetime.utcnow().isoformat()
                })

        except Exception as e:
            # Fail silently; other sources will still work
            continue

    return news_items
