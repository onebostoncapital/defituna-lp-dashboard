from data.sources.coingecko import get_sol_price_coingecko, get_sol_price_history_coingecko
from data.sources.yfinance_source import get_sol_price_yfinance, get_sol_price_history_yfinance


def get_sol_price():
    """
    Get latest SOL price with fallback between sources.
    """
    price = get_sol_price_coingecko()
    if price is not None:
        return price

    return get_sol_price_yfinance()


def get_sol_price_history(days: int = 200):
    """
    Get historical SOL price data with fallback.
    Returns pandas DataFrame with 'close' column.
    """
    data = get_sol_price_history_coingecko(days)
    if data is not None and not data.empty:
        return data

    return get_sol_price_history_yfinance(days)
