import pandas as pd


def calculate_volatility_regime(close: pd.Series) -> str:
    """
    Classifies volatility regime based on rolling std deviation.
    """

    if close is None or len(close) < 30:
        return "Unavailable"

    returns = close.pct_change().dropna()
    vol = returns.rolling(20).std().iloc[-1]

    if pd.isna(vol):
        return "Unavailable"

    if vol < 0.01:
        return "Low"
    elif vol < 0.025:
        return "Normal"
    else:
        return "High"
