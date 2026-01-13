import yfinance as yf
import pandas as pd


def fetch_price_history(symbol: str, days: int = 7) -> pd.DataFrame:
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=f"{days}d", interval="1h")

        if df.empty:
            raise ValueError("Empty data from yFinance")

        df = df.rename(columns={"Close": "close"})
        df = df[["close"]]

        return df

    except Exception as e:
        raise RuntimeError(f"yFinance price fetch failed: {e}")
