import pandas as pd

def trend_strength(price_series: pd.Series) -> str:
    if len(price_series) < 20:
        return "Insufficient data"

    momentum = price_series.iloc[-1] - price_series.iloc[-20]

    if momentum > 0:
        return "Bullish"
    elif momentum < 0:
        return "Bearish"
    return "Neutral"
