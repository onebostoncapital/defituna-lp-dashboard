import pandas as pd


def calculate_ma200(price_series: pd.DataFrame):
    """
    Calculate MA200 signal using the latest price only.
    """

    if price_series is None or price_series.empty:
        return {
            "signal": "Neutral",
            "score": 0,
            "driver": "MA200 data unavailable"
        }

    close = price_series["close"]

    ma200 = close.rolling(window=200).mean()

    latest_price = close.iloc[-1]
    latest_ma200 = ma200.iloc[-1]

    if pd.isna(latest_ma200):
        return {
            "signal": "Neutral",
            "score": 0,
            "driver": "MA200 insufficient data"
        }

    distance_pct = ((latest_price - latest_ma200) / latest_ma200) * 100

    if distance_pct > 1.0:
        return {
            "signal": "Bullish",
            "score": 25,
            "driver": "Price above MA200"
        }

    if distance_pct < -1.0:
        return {
            "signal": "Bearish",
            "score": -25,
            "driver": "Price below MA200"
        }

    return {
        "signal": "Neutral",
        "score": 0,
        "driver": "Price near MA200"
    }
