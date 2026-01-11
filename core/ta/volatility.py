import pandas as pd


def calculate_volatility(price_series: pd.DataFrame, window: int = 20):
    """
    Calculate volatility regime using latest volatility value only.
    """

    if price_series is None or price_series.empty:
        return {
            "signal": "Neutral",
            "score": 0,
            "driver": "Volatility data unavailable"
        }

    close = price_series["close"]

    returns = close.pct_change()

    volatility_series = returns.rolling(window=window).std() * 100
    latest_volatility = volatility_series.iloc[-1]

    if pd.isna(latest_volatility):
        return {
            "signal": "Neutral",
            "score": 0,
            "driver": "Volatility insufficient data"
        }

    volatility = float(latest_volatility)

    if volatility < 1.5:
        return {
            "signal": "Bullish",
            "score": 10,
            "driver": "Low volatility regime"
        }

    if volatility > 4.0:
        return {
            "signal": "Bearish",
            "score": -10,
            "driver": "High volatility regime"
        }

    return {
        "signal": "Neutral",
        "score": 0,
        "driver": "Moderate volatility"
    }
