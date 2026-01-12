# =================================================
# STREAMLIT CLOUD PATH FIX (MUST BE FIRST)
# =================================================
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

# =================================================
# STANDARD IMPORTS
# =================================================
import streamlit as st

from data.store.price_store import (
    get_current_price,
    get_price_history
)

from core.strategy.fusion_engine import fuse_signals

# =================================================
# STREAMLIT SETUP
# =================================================
st.set_page_config(
    page_title="DefiTuna LP Dashboard",
    layout="wide"
)

st.title("DefiTuna LP Dashboard")
st.caption("Multi-Range Liquidity Intelligence System")

# =================================================
# FETCH PRICE DATA (FROM STORE ONLY)
# =================================================
with st.spinner("Fetching SOL price data..."):
    current_price = get_current_price()
    price_history = get_price_history(days=200)

if current_price is None or price_history is None:
    st.error("Price data unavailable.")
    st.stop()

# =================================================
# CORE ENGINE
# =================================================
fusion_output = fuse_signals(price_history)

# =================================================
# SECTION 1 — PRICE
# =================================================
st.markdown("## 🔵 Solana (SOL) Price")
st.metric("Current Price", f"${current_price:,.2f}")

# =================================================
# SECTION 2 — MARKET STATE
# =================================================
st.markdown("## 📈 Market State")
st.write(f"**Direction:** {fusion_output['final_direction']}")
st.write(f"**Regime:** {fusion_output['risk_mode']}")
st.write(f"**Confidence:** {fusion_output['final_confidence']}")

# =================================================
# SECTION 3 — ACTIVE STRATEGY
# =================================================
st.markdown("## ⭐ Active LP Strategy")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Active Mode", fusion_output["active_mode"])
col2.metric("Range Low", f"${fusion_output['active_range']['range_low']}")
col3.metric("Range High", f"${fusion_output['active_range']['range_high']}")
col4.metric("Width (%)", fusion_output["active_range"]["width_pct"])

st.write(
    f"**Capital Allocation:** {int(fusion_output['active_allocation'] * 100)}%  \n"
    f"**Liquidity Floor:** {int(fusion_output['active_range']['liquidity_floor'] * 100)}%"
)

st.info(fusion_output["active_reason"])

st.divider()

# =================================================
# SECTION 4 — MULTI-RANGE VIEW
# =================================================
st.markdown("## 🧩 Liquidity Ranges (All Modes)")

ranges = fusion_output["multi_ranges"]["ranges"]
allocation = fusion_output["multi_ranges"]["allocation"]
active_mode = fusion_output["active_mode"]

for mode in ["Defensive", "Balanced", "Aggressive"]:
    is_active = mode == active_mode

    st.subheader(f"{mode} {'⭐ ACTIVE' if is_active else ''}")

    col1, col2, col3 = st.columns(3)
    col1.metric("Range Low", f"${ranges[mode]['range_low']}")
    col2.metric("Range High", f"${ranges[mode]['range_high']}")
    col3.metric("Width (%)", ranges[mode]["width_pct"])

    st.write(
        f"Liquidity Allocation: {int(allocation[mode] * 100)}%  "
        f"(Floor: {int(ranges[mode]['liquidity_floor'] * 100)}%)"
    )

    if is_active:
        st.success("This mode is currently ACTIVE")

    st.divider()

# =================================================
# SECTION 5 — TECHNICAL SUMMARY
# =================================================
st.markdown("## 📊 Technical Analysis Summary")

col1, col2, col3 = st.columns(3)
col1.metric("TA Score", fusion_output["ta_score"])
col2.metric("Volatility Regime", fusion_output["volatility_regime"])
col3.metric("Trend Strength", fusion_output["trend_strength"])

# =================================================
# SECTION 6 — TECHNICAL DRIVERS
# =================================================
st.markdown("## 🧮 Technical Drivers")
for driver in fusion_output["ta_drivers"]:
    st.write(f"• {driver}")

# =================================================
# FOOTNOTE
# =================================================
st.caption(
    "ℹ️ LP mode and ranges are selected automatically based on "
    "technical signals, volatility, confidence, and detected market regime."
)
