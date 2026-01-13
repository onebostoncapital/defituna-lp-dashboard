# app/main.py

import os
import sys
import streamlit as st

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from data.store import get_current_price, get_price_history
from core.strategy.fusion_engine import fuse_signals

# ---------------------------------------------
# STREAMLIT SETUP
# ---------------------------------------------

st.set_page_config(page_title="DeFiTuna LP Dashboard", layout="wide")
st.title("DeFiTuna LP Dashboard")
st.caption("Multi-Range Liquidity Intelligence System")

symbol = "solana"

# ---------------------------------------------
# PRICE FETCH
# ---------------------------------------------

with st.spinner("Fetching price data..."):
    current_price = get_current_price(symbol)
    price_history = get_price_history(symbol, days=7)

if current_price is None or price_history is None:
    st.error("Price data unavailable.")
    st.stop()

# ---------------------------------------------
# CORE ENGINE
# ---------------------------------------------

fusion_output = fuse_signals(price_history)

# ---------------------------------------------
# DISPLAY
# ---------------------------------------------

st.subheader("SOL Price")
st.metric("Current Price", f"${current_price:,.2f}")

st.subheader("Market State")
st.write("Direction:", fusion_output.get("direction", "N/A"))
st.write("Regime:", fusion_output.get("regime", "N/A"))
st.write("Confidence:", fusion_output.get("confidence", 0.0))
