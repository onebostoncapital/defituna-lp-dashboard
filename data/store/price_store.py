from data.router.price_router import (
    get_sol_price,
    get_sol_price_history
)

def get_current_price():
    price = get_sol_price()
    if price is None:
        return None
    return float(price)

def get_price_history(days=200):
    history = get_sol_price_history(days)
    if history is None or len(history) == 0:
        return None
    return history
