import streamlit as st

from data.store.price_store import get_current_price, get_price_history
from core.ta.ta_aggregator import run_ta

st.set_page_config(page_title="DeFiTuna LP Dashboard", layout="wide")

st.title("DeFiTuna LP Dashboard")
st.caption("Multi-Range Liquidity Intelligence System")

symbol = "sol"

price = get_current_price(symbol)
if price is None:
    st.error("Price data unavailable")
    st.stop()

st.subheader("SOL Price")
st.metric("Current Price", f"${price:.2f}")

price_history = get_price_history(symbol, days=30)
ta = run_ta(price_history)

st.subheader("Technical Analysis")
st.metric("TA Score", ta["ta_score"])
st.write("Volatility Regime:", ta["volatility"])
st.write("Trend Strength:", ta["trend"])

st.subheader("Technical Drivers")
for d in ta["drivers"]:
    st.write(f"- {d}")
