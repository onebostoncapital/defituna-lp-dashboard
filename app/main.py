# app/main.py

import sys
from pathlib import Path

# ==================================================
# FIX PYTHON PATH FOR STREAMLIT
# ==================================================

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

# ==================================================
# STANDARD IMPORTS
# ==================================================

import streamlit as st

from data.store.price_store import (
    get_current_price,
    get_price_history,
)

from core.strategy.fusion_engine import fuse_signals

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="DeFiTuna LP Dashboard",
    layout="wide",
)

st.title("DeFiTuna LP Dashboard")
st.caption("Multi-Range Liquidity Intelligence System")

# ==================================================
# FETCH PRICE DATA
# ==================================================

symbol = "SOL"

current_price = get_current_price(symbol)
price_history = get_price_history(symbol, days=7)

if current_price is None or price_history.empty:
    st.error("Price data unavailable.")
    st.stop()

# ==================================================
# PRICE DISPLAY
# ==================================================

st.subheader(f"{symbol} Price")
st.metric("Current Price", f"${current_price:,.2f}")

# ==================================================
# RUN STRATEGY ENGINE
# ==================================================

fusion_output = fuse_signals(price_history)

# ==================================================
# MARKET STATE
# ==================================================

st.subheader("Market State")

c1, c2, c3 = st.columns(3)

c1.metric("Direction", fusion_output.get("direction", "N/A"))
c2.metric("Regime", fusion_output.get("regime", "N/A"))
c3.metric("Confidence", fusion_output.get("confidence", 0.0))

# ==================================================
# ACTIVE STRATEGY
# ==================================================

st.subheader("Active LP Strategy")

st.metric("Mode", fusion_output.get("active_mode", "N/A"))
st.metric("Capital Allocation (%)", fusion_output.get("capital_pct", 0))
st.metric("Liquidity Floor (%)", fusion_output.get("liquidity_floor_pct", 0))

if fusion_output.get("active_reason"):
    st.info(fusion_output["active_reason"])

# ==================================================
# MULTI-RANGE COMPARISON
# ==================================================

st.subheader("Liquidity Ranges (All Modes)")

ranges = fusion_output.get("ranges", {})

if not ranges:
    st.warning("Range engine not active yet.")
else:
    for mode, r in ranges.items():
        st.markdown(f"### {mode} Mode")
        cols = st.columns(3)
        cols[0].metric("Low", f"${r['low']:,.2f}")
        cols[1].metric("High", f"${r['high']:,.2f}")
        cols[2].metric("Width (%)", r["width_pct"])

# ==================================================
# TECHNICAL SUMMARY
# ==================================================

st.subheader("Technical Analysis")

st.metric("TA Score", fusion_output.get("ta_score", 0))
st.metric("Volatility Regime", fusion_output.get("volatility_regime", "N/A"))
st.metric("Trend Strength", fusion_output.get("trend_strength", "N/A"))

# ==================================================
# TECHNICAL DRIVERS
# ==================================================

st.subheader("Technical Drivers")

ta_drivers = fusion_output.get("ta_drivers", [])
if ta_drivers:
    for d in ta_drivers:
        st.write("•", d)
else:
    st.write("No technical drivers available.")

# ==================================================
# FUNDAMENTAL DRIVERS
# ==================================================

fa_drivers = fusion_output.get("fa_drivers", [])
if fa_drivers:
    st.subheader("Fundamental Drivers")
    for d in fa_drivers:
        st.write("•", d)
