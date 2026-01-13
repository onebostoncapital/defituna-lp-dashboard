import pandas as pd


def calculate_trend_strength(close: pd.Series) -> dict:
    """
    Measures trend strength using price displacement.
    """

    if close is None or len(close) < 30:
        return {"signal": "Unavailable"}

    recent = close.iloc[-1]
    past = close.iloc[-20]

    delta = (recent - past) / past

    if delta > 0.03:
        return {"signal": "Bullish"}
    elif delta < -0.03:
        return {"signal": "Bearish"}
    else:
        return {"signal": "Neutral"}
