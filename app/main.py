import streamlit as st

from data.store.price_store import get_current_price, get_price_history
from core.ta.ta_aggregator import aggregate_ta_signals

st.set_page_config(page_title="DeFiTuna LP Dashboard", layout="wide")

st.title("DeFiTuna LP Dashboard")
st.caption("Multi-Range Liquidity Intelligence System")

symbol = "SOL"

current_price = get_current_price(symbol)
price_history = get_price_history(symbol, days=30)

st.subheader("SOL Price")
st.metric("Current Price", f"${current_price:,.2f}")

ta = aggregate_ta_signals(price_history)

st.subheader("Technical Analysis")
st.metric("TA Score", ta["score"])
st.write("Volatility Regime:", ta["volatility_regime"])
st.write("Trend Strength:", ta["trend_strength"])

st.subheader("Technical Drivers")
for d in ta["drivers"]:
    st.write("•", d)
