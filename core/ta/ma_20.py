import pandas as pd

def ma_20(price_series: pd.Series) -> bool | None:
    if len(price_series) < 20:
        return None
    return price_series.iloc[-1] > price_series.rolling(20).mean().iloc[-1]
