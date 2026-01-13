import pandas as pd

def ma_200(price_series: pd.Series) -> bool | None:
    if len(price_series) < 200:
        return None
    return price_series.iloc[-1] > price_series.rolling(200).mean().iloc[-1]
