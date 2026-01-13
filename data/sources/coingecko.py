# data/sources/coingecko.py

import requests

BASE_URL = "https://api.coingecko.com/api/v3"


def get_current_price_from_coingecko(symbol: str) -> float:
    url = f"{BASE_URL}/simple/price"
    params = {
        "ids": symbol.lower(),
        "vs_currencies": "usd"
    }
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()
    return data[symbol.lower()]["usd"]


def get_price_history_from_coingecko(symbol: str, days: int):
    url = f"{BASE_URL}/coins/{symbol.lower()}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": days
    }
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()
    return data.get("prices", [])
