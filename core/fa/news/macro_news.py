import feedparser
from datetime import datetime


MACRO_RSS_FEEDS = {
    "Reuters": "https://www.reuters.com/markets/rss",
    "CNBC": "https://www.cnbc.com/id/10001147/device/rss/rss.html"
}

RISK_OFF_KEYWORDS = [
    "inflation", "rate hike", "tightening", "recession",
    "crisis", "selloff", "geopolitical", "war", "sanctions"
]

RISK_ON_KEYWORDS = [
    "rate cut", "stimulus", "easing", "growth",
    "recovery", "liquidity", "support"
]

HIGH_IMPACT_KEYWORDS = [
    "fed", "fomc", "cpi", "interest rate", "central bank"
]


def score_macro_headline(headline: str):
    """
    Score macro news headline for crypto spillover risk.
    """

    headline_lower = headline.lower()

    risk_off_hits = sum(word in headline_lower for word in RISK_OFF_KEYWORDS)
    risk_on_hits = sum(word in headline_lower for word in RISK_ON_KEYWORDS)
    high_impact_hits = sum(word in headline_lower for word in HIGH_IMPACT_KEYWORDS)

    if risk_off_hits > risk_on_hits and risk_off_hits > 0:
        bias = "Risk-Off"
        base_score = -25
    elif risk_on_hits > risk_off_hits and risk_on_hits > 0:
        bias = "Risk-On"
        base_score = 20
    else:
        bias = "Neutral"
        base_score = 0

    severity = "High" if high_impact_hits > 0 else "Medium" if abs(base_score) > 0 else "Low"

    score = base_score - (high_impact_hits * 5) if bias == "Risk-Off" else base_score + (high_impact_hits * 5)
    score = max(min(score, 40), -40)

    confidence = min(abs(score) / 40, 1.0)

    return bias, severity, score, round(confidence, 2)


def fetch_macro_news(limit_per_source: int = 5):
    """
    Fetch and score macro / TradFi news from multiple RSS sources.
    """

    macro_items = []

    for source, url in MACRO_RSS_FEEDS.items():
        try:
            feed = feedparser.parse(url)

            for entry in feed.entries[:limit_per_source]:
                headline = entry.title
                published = entry.get("published", None)

                bias, severity, score, confidence = score_macro_headline(headline)

                macro_items.append({
                    "event": headline,
                    "source": source,
                    "risk_bias": bias,
                    "severity": severity,
                    "score": score,
                    "confidence": confidence,
                    "timestamp": published or datetime.utcnow().isoformat()
                })

        except Exception:
            continue

    return macro_items
