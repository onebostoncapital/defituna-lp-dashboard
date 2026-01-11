from core.fa.news.crypto_news import fetch_crypto_news
from core.fa.news.macro_news import fetch_macro_news
from core.fa.news.geopolitical_news import fetch_geopolitical_news
from core.fa.calendar.economic_calendar import fetch_economic_events


def aggregate_fa_signals():
    """
    Aggregate all Fundamental Analysis signals into one FA score.
    """

    score = 0.0
    drivers = []

    # -----------------------------
    # Crypto News
    # -----------------------------
    crypto = fetch_crypto_news()
    if crypto:
        score += crypto.get("score", 0.0)
        drivers.append("Crypto news impact")

    # -----------------------------
    # Macro News
    # -----------------------------
    macro = fetch_macro_news()
    if macro:
        score += macro.get("score", 0.0)
        drivers.append("Macro news impact")

    # -----------------------------
    # Geopolitical News
    # -----------------------------
    geo = fetch_geopolitical_news()
    if geo:
        score += geo.get("score", 0.0)
        drivers.append("Geopolitical risk")

    # -----------------------------
    # Economic Calendar
    # -----------------------------
    calendar = fetch_economic_events()
    if calendar:
        score += calendar.get("score", 0.0)
        drivers.append("Economic events")

    return {
        "fa_score": round(score, 3),
        "drivers": drivers
    }
