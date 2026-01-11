import pandas as pd


def calculate_ma_crossover(price_series: pd.DataFrame):
    """
    Calculate MA20 / MA200 crossover signal using latest values only.
    """

    if price_series is None or price_series.empty:
        return {
            "signal": "Neutral",
            "score": 0,
            "driver": "MA crossover data unavailable"
        }

    close = price_series["close"]

    ma20 = close.rolling(window=20).mean()
    ma200 = close.rolling(window=200).mean()

    latest_ma20 = ma20.iloc[-1]
    latest_ma200 = ma200.iloc[-1]

    if pd.isna(latest_ma20) or pd.isna(latest_ma200):
        return {
            "signal": "Neutral",
            "score": 0,
            "driver": "MA crossover insufficient data"
        }

    diff_pct = float((latest_ma20 - latest_ma200) / latest_ma200 * 100)

    if diff_pct > 0.5:
        return {
            "signal": "Bullish",
            "score": 20,
            "driver": "MA20 above MA200"
        }

    if diff_pct < -0.5:
        return {
            "signal": "Bearish",
            "score": -20,
            "driver": "MA20 below MA200"
        }

    return {
        "signal": "Neutral",
        "score": 0,
        "driver": "MA20 and MA200 converging"
    }
