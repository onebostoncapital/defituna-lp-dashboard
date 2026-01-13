import pandas as pd

def calculate_rsi(price_series: pd.Series, period: int = 14) -> float | None:
    if len(price_series) < period + 1:
        return None

    delta = price_series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return float(rsi.iloc[-1])
