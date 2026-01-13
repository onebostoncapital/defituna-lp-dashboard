import yfinance as yf

def get_sol_price():
    try:
        ticker = yf.Ticker("SOL-USD")
        data = ticker.history(period="1d", interval="1m")
        if data.empty:
            return None
        return float(data["Close"].iloc[-1])
    except Exception:
        return None
