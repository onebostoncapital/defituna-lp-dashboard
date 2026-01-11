import yfinance as yf
import pandas as pd


def get_sol_price_yfinance():
    """
    Fetch current SOL price using Yahoo Finance.
    """
    try:
        ticker = yf.Ticker("SOL-USD")
        price = ticker.history(period="1d")["Close"].iloc[-1]
        return float(price)
    except Exception:
        return None


def get_sol_price_history_yfinance(days: int = 200):
    """
    Fetch historical SOL price data using Yahoo Finance.
    Returns DataFrame with 'close' column.
    """
    try:
        ticker = yf.Ticker("SOL-USD")
        df = ticker.history(period=f"{days}d")

        if df.empty:
            return None

        df = df[["Close"]]
        df.rename(columns={"Close": "close"}, inplace=True)

        return df
    except Exception:
        return None
