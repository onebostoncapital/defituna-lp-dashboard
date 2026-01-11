from core.fa.news.crypto_news import fetch_crypto_news
from core.fa.news.macro_news import fetch_macro_news
from core.fa.news.geopolitical_news import fetch_geopolitical_news
from core.fa.calendar.economic_calendar import detect_upcoming_events


def aggregate_fa_signals():
    """
    Aggregate Fundamental Analysis signals into one FA decision.

    Output (dict):
        - fa_bias: Bullish / Bearish / Neutral
        - fa_score: int (-100 to +100)
        - confidence: float (0 to 1)
        - risk_flags: list of strings
    """

    crypto_news = fetch_crypto_news()
    macro_news = fetch_macro_news()
    geo_news = fetch_geopolitical_news()
    calendar_events = detect_upcoming_events()

    fa_score = 0
    risk_flags = []

    # --------------------------------------------------
    # 1. Calendar risk (HIGHEST PRIORITY)
    # --------------------------------------------------
    if calendar_events:
        fa_score -= 50
        risk_flags.append("HIGH_IMPACT_CALENDAR_EVENT")

    # --------------------------------------------------
    # 2. Geopolitical risk (VERY HIGH PRIORITY)
    # --------------------------------------------------
    geo_score = sum(item["score"] for item in geo_news)
    if geo_score < -20:
        risk_flags.append("GEO_RISK_HIGH")

    fa_score += geo_score * 0.6

    # --------------------------------------------------
    # 3. Macro news impact
    # --------------------------------------------------
    macro_score = sum(item["score"] for item in macro_news)
    if macro_score < -30:
        risk_flags.append("MACRO_RISK_OFF")
    elif macro_score > 30:
        risk_flags.append("MACRO_RISK_ON")

    fa_score += macro_score * 0.4

    # --------------------------------------------------
    # 4. Crypto news impact (LOWEST PRIORITY)
    # --------------------------------------------------
    crypto_score = sum(item["score"] for item in crypto_news)
    fa_score += crypto_score * 0.25

    # Clamp FA score
    fa_score = max(min(fa_score, 100), -100)

    # --------------------------------------------------
    # 5. Determine FA bias
    # --------------------------------------------------
    if fa_score > 25:
        fa_bias = "Bullish"
    elif fa_score < -25:
        fa_bias = "Bearish"
    else:
        fa_bias = "Neutral"

    # --------------------------------------------------
    # 6. Confidence calculation
    # --------------------------------------------------
    confidence = min(abs(fa_score) / 100, 1.0)

    if "HIGH_IMPACT_CALENDAR_EVENT" in risk_flags:
        confidence *= 0.5

    if "GEO_RISK_HIGH" in risk_flags:
        confidence *= 0.7

    return {
        "fa_bias": fa_bias,
        "fa_score": round(fa_score, 2),
        "confidence": round(confidence, 2),
        "risk_flags": risk_flags
    }
