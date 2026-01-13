# app/main.py
import sys
import os

# -------------------------------------------------------------------
# FIX IMPORT PATH (DO NOT REMOVE)
# -------------------------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st

from data.store.price_store import get_current_price, get_price_history
from core.strategy.fusion_engine import fuse_signals

# -------------------------------------------------------------------
# UI CONFIG
# -------------------------------------------------------------------
st.set_page_config(page_title="DeFiTuna LP Dashboard", layout="wide")

st.title("DeFiTuna LP Dashboard")
st.caption("Multi-Range Liquidity Intelligence System")

symbol = "SOL"

# -------------------------------------------------------------------
# PRICE
# -------------------------------------------------------------------
try:
    current_price = get_current_price(symbol)
    st.subheader("SOL Price")
    st.metric("Current Price", f"${current_price:.2f}")
except Exception as e:
    st.error(f"Price layer failed: {e}")
    st.stop()

# -------------------------------------------------------------------
# PRICE HISTORY
# -------------------------------------------------------------------
try:
    price_history = get_price_history(symbol, days=7)
except Exception as e:
    st.error(f"Price history failed: {e}")
    st.stop()

# -------------------------------------------------------------------
# STRATEGY ENGINE
# -------------------------------------------------------------------
try:
    fusion_output = fuse_signals(price_history)
except Exception as e:
    st.error(f"Strategy engine failed: {e}")
    st.stop()

# -------------------------------------------------------------------
# MARKET STATE (FIXED RENDERING)
# -------------------------------------------------------------------
st.subheader("Market State")
c1, c2, c3 = st.columns(3)

c1.markdown(f"**Direction**  \n{fusion_output.get('direction', 'N/A')}")
c2.markdown(f"**Regime**  \n{fusion_output.get('regime', 'N/A')}")
c3.markdown(f"**Confidence**  \n{fusion_output.get('confidence', 0.0)}")

# -------------------------------------------------------------------
# ACTIVE STRATEGY
# -------------------------------------------------------------------
st.subheader("Active LP Strategy")

strategy = fusion_output.get("strategy", {})

st.markdown(f"**Mode:** {strategy.get('mode', 'Unavailable')}")
st.markdown(f"**Capital Allocation (%):** {strategy.get('capital_pct', 0)}")
st.markdown(f"**Liquidity Floor (%):** {strategy.get('liquidity_floor_pct', 0)}")

# -------------------------------------------------------------------
# TECHNICAL ANALYSIS
# -------------------------------------------------------------------
st.subheader("Technical Analysis")

ta = fusion_output.get("ta", {})

st.markdown(f"**TA Score:** {ta.get('score', 0)}")
st.markdown(f"**Volatility Regime:** {ta.get('volatility_regime', 'Unavailable')}")
st.markdown(f"**Trend Strength:** {ta.get('trend_strength', 'Unavailable')}")

drivers = ta.get("drivers", [])

if drivers:
    st.subheader("Technical Drivers")
    for d in drivers:
        st.markdown(f"- {d}")
else:
    st.caption("No technical drivers available.")
