import pandas as pd
from typing import Optional

# ==============================
# INTERNAL NORMALIZATION (CORE)
# ==============================

def _normalize_price_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    GUARANTEE:
    - Return a DataFrame
    - Must contain column: 'close'
    - Must be numeric
    - Must be clean (no NaN)
    """

    if df is None or df.empty:
        return pd.DataFrame(columns=["close"])

    # If already correct
    if "close" in df.columns:
        close = df["close"]

    # Common alternative names
    elif "price" in df.columns:
        close = df["price"]

    elif "Close" in df.columns:
        close = df["Close"]

    # If single column dataframe
    elif df.shape[1] == 1:
        close = df.iloc[:, 0]

    else:
        # Hard fail-safe
        return pd.DataFrame(columns=["close"])

    close = pd.to_numeric(close, errors="coerce").dropna()

    return pd.DataFrame({"close": close})


# ==============================
# PRICE SOURCES
# ==============================

def _fetch_from_coingecko(days: int) -> pd.DataFrame:
    from data.sources.coingecko import fetch_price_history

    raw = fetch_price_history(days=days)

    if isinstance(raw, list):
        # CoinGecko format: [[timestamp, price], ...]
        prices = [p[1] for p in raw]
        return pd.DataFrame({"close": prices})

    return raw


def _fetch_from_yfinance(days: int) -> pd.DataFrame:
    from data.sources.yfinance_source import fetch_price_history

    return fetch_price_history(days=days)


# ==============================
# PUBLIC API (ONLY THESE ARE USED)
# ==============================

def get_price_history(
    days: int = 7,
    source: str = "coingecko"
) -> pd.DataFrame:
    """
    ALWAYS returns:
    DataFrame with column: ['close']
    """

    try:
        if source == "yfinance":
            raw_df = _fetch_from_yfinance(days)
        else:
            raw_df = _fetch_from_coingecko(days)

        return _normalize_price_df(raw_df)

    except Exception:
        # Absolute safety
        return pd.DataFrame(columns=["close"])


def get_current_price(source: str = "coingecko") -> Optional[float]:
    """
    ALWAYS returns:
    - float price OR None
    """

    df = get_price_history(days=1, source=source)

    if df.empty:
        return None

    return float(df["close"].iloc[-1])
