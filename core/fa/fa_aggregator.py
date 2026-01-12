from core.fa.news.crypto_news import fetch_crypto_news
from core.fa.news.macro_news import fetch_macro_news
from core.fa.news.geopolitical_news import fetch_geopolitical_news
from core.fa.calendar.economic_calendar import fetch_economic_events


def aggregate_fa_signals():
    """
    Aggregates all Fundamental Analysis signals.
    ALWAYS returns:
    - fa_score (float)
    - drivers (list of strings)
    """

    score = 0.0
    drivers = []

    # -----------------------------
    # CRYPTO NEWS
    # -----------------------------
    crypto = fetch_crypto_news()
    if crypto:
        score += crypto.get("score", 0.0)
        drivers.extend(crypto.get("drivers", []))

    # -----------------------------
    # MACRO NEWS
    # -----------------------------
    macro = fetch_macro_news()
    if macro:
        score += macro.get("score", 0.0)
        drivers.extend(macro.get("drivers", []))

    # -----------------------------
    # GEOPOLITICAL RISK
    # -----------------------------
    geo = fetch_geopolitical_news()
    if geo:
        score += geo.get("score", 0.0)
        drivers.extend(geo.get("drivers", []))

    # -----------------------------
    # ECONOMIC CALENDAR
    # -----------------------------
    calendar = fetch_economic_events()
    if calendar:
        score += calendar.get("score", 0.0)
        drivers.extend(calendar.get("drivers", []))

    return {
        "fa_score": round(score, 2),
        "drivers": drivers if drivers else ["No dominant fundamental events detected"]
    }
