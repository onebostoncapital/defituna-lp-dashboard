import pandas as pd


def calculate_ma20(price_series: pd.DataFrame):
    """
    Calculate MA20 signal using the latest price only.
    """

    if price_series is None or price_series.empty:
        return {
            "signal": "Neutral",
            "score": 0,
            "driver": "MA20 data unavailable"
        }

    close = price_series["close"]

    ma20 = close.rolling(window=20).mean()

    latest_price = close.iloc[-1]
    latest_ma20 = ma20.iloc[-1]

    if pd.isna(latest_ma20):
        return {
            "signal": "Neutral",
            "score": 0,
            "driver": "MA20 insufficient data"
        }

    distance_pct = ((latest_price - latest_ma20) / latest_ma20) * 100

    if distance_pct > 0.5:
        return {
            "signal": "Bullish",
            "score": 15,
            "driver": "Price above MA20"
        }

    if distance_pct < -0.5:
        return {
            "signal": "Bearish",
            "score": -15,
            "driver": "Price below MA20"
        }

    return {
        "signal": "Neutral",
        "score": 0,
        "driver": "Price near MA20"
    }
