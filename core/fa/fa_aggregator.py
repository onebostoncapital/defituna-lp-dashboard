"""
Fundamental Analysis Aggregator
CACHED + RESILIENT MODE

This module guarantees:
- No crashes
- No missing keys
- Safe defaults when news APIs fail
"""

def aggregate_fa_signals():
    """
    Always returns a complete FA dictionary.
    Never throws KeyError.
    """

    # -----------------------------
    # SAFE DEFAULTS
    # -----------------------------
    crypto_score = 0.0
    macro_score = 0.0
    geo_score = 0.0

    crypto_drivers = []
    macro_drivers = []
    geo_drivers = []

    # -----------------------------
    # CRYPTO NEWS
    # -----------------------------
    try:
        from core.fa.news.crypto_news import fetch_crypto_news
        crypto = fetch_crypto_news() or {}
        crypto_score = float(crypto.get("score", 0.0))
        crypto_drivers = crypto.get("drivers", [])
    except Exception:
        pass

    # -----------------------------
    # MACRO NEWS
    # -----------------------------
    try:
        from core.fa.news.macro_news import fetch_macro_news
        macro = fetch_macro_news() or {}
        macro_score = float(macro.get("score", 0.0))
        macro_drivers = macro.get("drivers", [])
    except Exception:
        pass

    # -----------------------------
    # GEOPOLITICAL NEWS
    # -----------------------------
    try:
        from core.fa.news.geopolitical_news import fetch_geopolitical_news
        geo = fetch_geopolitical_news() or {}
        geo_score = float(geo.get("score", 0.0))
        geo_drivers = geo.get("drivers", [])
    except Exception:
        pass

    # -----------------------------
    # FINAL FA SCORE
    # -----------------------------
    fa_score = round(
        crypto_score + macro_score + geo_score,
        2
    )

    # -----------------------------
    # RETURN (LOCKED CONTRACT)
    # -----------------------------
    return {
        "fa_score": fa_score,
        "crypto_score": crypto_score,
        "macro_score": macro_score,
        "geo_score": geo_score,
        "fa_drivers": (
            crypto_drivers +
            macro_drivers +
            geo_drivers
        )
    }
