import pandas as pd


def calculate_trend_strength(price_series: pd.DataFrame, window: int = 20):
    """
    Calculate trend strength using directional movement consistency.
    Uses latest value only.
    """

    if price_series is None or price_series.empty:
        return {
            "signal": "Neutral",
            "score": 0,
            "driver": "Trend data unavailable"
        }

    close = price_series["close"]

    price_diff = close.diff()

    up_moves = price_diff.where(price_diff > 0, 0)
    down_moves = -price_diff.where(price_diff < 0, 0)

    up_strength = up_moves.rolling(window=window).sum()
    down_strength = down_moves.rolling(window=window).sum()

    latest_up = up_strength.iloc[-1]
    latest_down = down_strength.iloc[-1]

    if pd.isna(latest_up) or pd.isna(latest_down):
        return {
            "signal": "Neutral",
            "score": 0,
            "driver": "Trend strength insufficient data"
        }

    total_strength = float(latest_up + latest_down)

    if total_strength == 0:
        return {
            "signal": "Neutral",
            "score": 0,
            "driver": "No directional movement"
        }

    dominance = (latest_up - latest_down) / total_strength

    if dominance > 0.3:
        return {
            "signal": "Bullish",
            "score": 10,
            "driver": "Strong upward trend"
        }

    if dominance < -0.3:
        return {
            "signal": "Bearish",
            "score": -10,
            "driver": "Strong downward trend"
        }

    return {
        "signal": "Neutral",
        "score": 0,
        "driver": "Weak or mixed trend"
    }
