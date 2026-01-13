import pandas as pd
from data.sources.coingecko import fetch_price_history

SUPPORTED_SYMBOLS = {
    "sol": "solana"
}

def get_price_history(symbol: str, days: int = 7) -> pd.DataFrame:
    symbol = symbol.lower()
    if symbol not in SUPPORTED_SYMBOLS:
        raise ValueError(f"Unsupported symbol: {symbol}")

    df = fetch_price_history(SUPPORTED_SYMBOLS[symbol], days=days)
    return df

def get_current_price(symbol: str) -> float | None:
    df = get_price_history(symbol, days=1)
    if df.empty:
        return None
    return float(df["price"].iloc[-1])
