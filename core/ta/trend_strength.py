import pandas as pd
import numpy as np


def calculate_trend_strength(price_series, lookback=20):
    """
    Trend strength calculated from a Pandas Series (MASTER RULE).
    """

    price_series = pd.to_numeric(price_series, errors="coerce").dropna()

    if len(price_series) < lookback:
        return {"signal": "Neutral", "confidence": 0.0}

    recent_prices = price_series.iloc[-lookback:]

    # Calculate directional movement
    price_changes = recent_prices.diff().dropna()

    up_moves = price_changes[price_changes > 0].sum()
    down_moves = abs(price_changes[price_changes < 0].sum())

    total_moves = up_moves + down_moves

    if total_moves == 0:
        return {"signal": "Neutral", "confidence": 0.0}

    strength_ratio = up_moves / total_moves

    if strength_ratio > 0.6:
        return {"signal": "Bullish", "confidence": round(strength_ratio, 2)}
    elif strength_ratio < 0.4:
        return {"signal": "Bearish", "confidence": round(1 - strength_ratio, 2)}
    else:
        return {"signal": "Neutral", "confidence": 0.5}
