from data.sources.coingecko import (
    fetch_sol_price,
    fetch_sol_price_history
)

def get_sol_price():
    return fetch_sol_price()

def get_sol_price_history(days=200):
    return fetch_sol_price_history(days)
