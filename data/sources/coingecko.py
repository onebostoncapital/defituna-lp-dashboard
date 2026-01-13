import requests

COINGECKO_PRICE_URL = (
    "https://api.coingecko.com/api/v3/simple/price"
)

def get_sol_price():
    try:
        params = {
            "ids": "solana",
            "vs_currencies": "usd"
        }
        r = requests.get(COINGECKO_PRICE_URL, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        return float(data["solana"]["usd"])
    except Exception:
        return None
