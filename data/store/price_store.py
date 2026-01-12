# data/store/price_store.py

import pandas as pd
from datetime import datetime, timezone

# ==============================
# SAFE IMPORTS (NO CRASH)
# ==============================

def _safe_import_coingecko():
    try:
        from data.sources.coingecko import (
            get_current_price as cg_current,
            get_price_history as cg_history,
        )
        return cg_current, cg_history
    except Exception:
        return None, None


def _safe_import_yfinance():
    try:
        from data.sources.yfinance_source import (
            get_current_price as yf_current,
            get_price_history as yf_history,
        )
        return yf_current, yf_history
    except Exception:
        return None, None


CG_CURRENT, CG_HISTORY = _safe_import_coingecko()
YF_CURRENT, YF_HISTORY = _safe_import_yfinance()

# ==============================
# CANONICAL OUTPUT CONTRACT
# ==============================

def _empty_price_df() -> pd.DataFrame:
    return pd.DataFrame(
        columns=["timestamp", "close"]
    )


def _normalize_series_to_df(series) -> pd.DataFrame:
    """
    Converts list / Series / DataFrame to canonical DataFrame:
    columns = ['timestamp', 'close']
    """
    try:
        if isinstance(series, pd.DataFrame):
            if "close" in series.columns:
                df = series.copy()
                if "timestamp" not in df.columns:
                    df["timestamp"] = pd.date_range(
                        end=datetime.now(timezone.utc),
                        periods=len(df),
                        freq="H",
                    )
                return df[["timestamp", "close"]]

        if isinstance(series, pd.Series):
            return pd.DataFrame(
                {
                    "timestamp": pd.date_range(
                        end=datetime.now(timezone.utc),
                        periods=len(series),
                        freq="H",
                    ),
                    "close": series.values,
                }
            )

        if isinstance(series, list):
            return pd.DataFrame(
                {
                    "timestamp": pd.date_range(
                        end=datetime.now(timezone.utc),
                        periods=len(series),
                        freq="H",
                    ),
                    "close": series,
                }
            )
    except Exception:
        pass

    return _empty_price_df()


# ==============================
# PUBLIC API (USED BY APP)
# ==============================

def get_current_price(symbol: str = "SOL") -> float | None:
    """
    Returns float price or None (never raises)
    """
    # Try CoinGecko
    if CG_CURRENT:
        try:
            price = CG_CURRENT(symbol)
            if isinstance(price, (int, float)):
                return float(price)
        except Exception:
            pass

    # Fallback Yahoo Finance
    if YF_CURRENT:
        try:
            price = YF_CURRENT(symbol)
            if isinstance(price, (int, float)):
                return float(price)
        except Exception:
            pass

    return None


def get_price_history(
    symbol: str = "SOL",
    days: int = 7,
) -> pd.DataFrame:
    """
    ALWAYS returns DataFrame with:
    ['timestamp', 'close']
    """

    # --- Try CoinGecko ---
    if CG_HISTORY:
        try:
            raw = CG_HISTORY(symbol, days=days)
            df = _normalize_series_to_df(raw)
            if not df.empty:
                return df
        except Exception:
            pass

    # --- Fallback Yahoo Finance ---
    if YF_HISTORY:
        try:
            raw = YF_HISTORY(symbol, days=days)
            df = _normalize_series_to_df(raw)
            if not df.empty:
                return df
        except Exception:
            pass

    # --- Last resort ---
    return _empty_price_df()
