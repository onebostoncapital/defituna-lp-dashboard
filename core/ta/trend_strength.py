def calculate_trend_strength(price_df):
    """
    Calculates simple momentum-based trend strength.
    Safe against short data series.
    """

    close = price_df["close"]

    # --- SAFETY GUARD
    if len(close) < 20:
        return {
            "score": 0,
            "label": "Neutral",
            "driver": "Trend strength unavailable (insufficient data)"
        }

    momentum = close.iloc[-1] - close.iloc[-20]

    if momentum > 0:
        return {
            "score": 1,
            "label": "Bullish",
            "driver": "Positive 20-period momentum"
        }
    elif momentum < 0:
        return {
            "score": -1,
            "label": "Bearish",
            "driver": "Negative 20-period momentum"
        }
    else:
        return {
            "score": 0,
            "label": "Neutral",
            "driver": "Flat momentum"
        }
