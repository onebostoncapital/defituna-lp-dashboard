import feedparser
from datetime import datetime


GEO_RSS_FEEDS = {
    "Reuters World": "https://www.reuters.com/world/rss",
    "AP World": "https://apnews.com/rss/apf-worldnews",
    "Al Jazeera": "https://www.aljazeera.com/xml/rss/all.xml"
}

HIGH_RISK_KEYWORDS = [
    "war", "conflict", "missile", "invasion", "airstrike",
    "sanction", "escalation", "military", "attack", "terror"
]

MEDIUM_RISK_KEYWORDS = [
    "tension", "protest", "strike", "border",
    "unrest", "diplomatic", "ceasefire"
]

REGION_KEYWORDS = {
    "Middle East": ["israel", "gaza", "iran", "iraq", "syria"],
    "Europe": ["ukraine", "russia", "nato"],
    "Asia": ["china", "taiwan", "korea"],
}


def detect_region(headline: str):
    headline_lower = headline.lower()
    for region, keywords in REGION_KEYWORDS.items():
        if any(word in headline_lower for word in keywords):
            return region
    return "Global"


def score_geopolitical_headline(headline: str):
    headline_lower = headline.lower()

    high_hits = sum(word in headline_lower for word in HIGH_RISK_KEYWORDS)
    medium_hits = sum(word in headline_lower for word in MEDIUM_RISK_KEYWORDS)

    if high_hits > 0:
        severity = "High"
        score = -40
    elif medium_hits > 0:
        severity = "Medium"
        score = -20
    else:
        severity = "Low"
        score = 0

    confidence = min(abs(score) / 40, 1.0)

    return severity, score, round(confidence, 2)


def fetch_geopolitical_news(limit_per_source: int = 5):
    """
    Fetch and score geopolitical news for crypto risk assessment.
    """

    geo_items = []

    for source, url in GEO_RSS_FEEDS.items():
        try:
            feed = feedparser.parse(url)

            for entry in feed.entries[:limit_per_source]:
                headline = entry.title
                published = entry.get("published", None)

                severity, score, confidence = score_geopolitical_headline(headline)

                if score < 0:  # only keep risk-relevant items
                    geo_items.append({
                        "event": headline,
                        "region": detect_region(headline),
                        "severity": severity,
                        "risk_bias": "Risk-Off",
                        "score": score,
                        "confidence": confidence,
                        "timestamp": published or datetime.utcnow().isoformat()
                    })

        except Exception:
            continue

    return geo_items
