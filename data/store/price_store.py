import pandas as pd

from data.sources.coingecko import fetch_price_history as cg_fetch
from data.sources.yfinance_source import fetch_price_history as yf_fetch


SYMBOL_MAP = {
    "SOL": {
        "coingecko": "solana",
        "yfinance": "SOL-USD"
    }
}


def get_price_history(symbol: str, days: int = 7) -> pd.DataFrame:
    if symbol not in SYMBOL_MAP:
        raise ValueError(f"Unsupported symbol: {symbol}")

    errors = []

    # 1️⃣ Try CoinGecko
    try:
        df = cg_fetch(SYMBOL_MAP[symbol]["coingecko"], days)
        if _validate_df(df):
            return df
    except Exception as e:
        errors.append(str(e))

    # 2️⃣ Fallback to yFinance
    try:
        df = yf_fetch(SYMBOL_MAP[symbol]["yfinance"], days)
        if _validate_df(df):
            return df
    except Exception as e:
        errors.append(str(e))

    raise RuntimeError("Price layer failed:\n" + "\n".join(errors))


def get_current_price(symbol: str) -> float:
    df = get_price_history(symbol, days=1)
    return float(df["close"].iloc[-1])


def _validate_df(df: pd.DataFrame) -> bool:
    return (
        isinstance(df, pd.DataFrame)
        and not df.empty
        and "close" in df.columns
    )
