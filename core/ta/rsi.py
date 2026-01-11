import pandas as pd


def calculate_rsi(price_series: pd.DataFrame, period: int = 14):
    """
    Calculate RSI signal using the latest RSI value only.
    """

    if price_series is None or price_series.empty:
        return {
            "signal": "Neutral",
            "score": 0,
            "driver": "RSI data unavailable"
        }

    close = price_series["close"]

    delta = close.diff()

    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    latest_rsi = rsi.iloc[-1]

    if pd.isna(latest_rsi):
        return {
            "signal": "Neutral",
            "score": 0,
            "driver": "RSI insufficient data"
        }

    current_rsi = float(latest_rsi)

    if current_rsi < 30:
        return {
            "signal": "Bullish",
            "score": 15,
            "driver": "RSI oversold"
        }

    if current_rsi > 70:
        return {
            "signal": "Bearish",
            "score": -15,
            "driver": "RSI overbought"
        }

    return {
        "signal": "Neutral",
        "score": 0,
        "driver": "RSI neutral"
    }
