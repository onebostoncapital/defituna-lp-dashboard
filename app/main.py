# =================================================
# STREAMLIT CLOUD IMPORT FIX (MUST BE FIRST)
# =================================================
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

# =================================================
# IMPORTS
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
# DATA FETCH
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
st.write(f"**Direction:** {fusion_output.get('final_direction')}")
st.write(f"**Regime:** {fusion_output.get('risk_mode')}")
st.write(f"**Confidence:** {fusion_output.get('final_confidence')}")

# =================================================
# SECTION 3 — ACTIVE LP STRATEGY
# =================================================
st.markdown("## ⭐ Active LP Strategy")

active_mode = fusion_output.get("active_mode")
active_range = fusion_output.get("active_range", {})
active_allocation = fusion_output.get("active_allocation", 0.0)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Active Mode", active_mode)
col2.metric("Range Low", f"${active_range.get('range_low', '—')}")
col3.metric("Range High", f"${active_range.get('range_high', '—')}")
col4.metric("Range Width (%)", f"{active_range.get('width_pct', '—')}")

st.write(f"**Capital Allocation:** {int(active_allocation * 100)}%")
st.write(
    f"**Liquidity Floor:** "
    f"{int(active_range.get('liquidity_floor', 0) * 100)}%"
)

st.info(
    f"**Why {active_mode} mode?** "
    "Selected automatically based on confidence, volatility, "
    "and detected market regime."
)

st.divider()

# =================================================
# SECTION 4 — MULTI-RANGE COMPARISON (RESTORED)
# =================================================
st.markdown("## 🧩 Liquidity Ranges (All Modes)")

multi_ranges = fusion_output.get("multi_ranges", {})
ranges = multi_ranges.get("ranges", {})
allocations = multi_ranges.get("allocation", {})

for mode in ["Defensive", "Balanced", "Aggressive"]:
    mode_range = ranges.get(mode, {})
    mode_alloc = allocations.get(mode, 0.0)
    is_active = mode == active_mode

    st.subheader(f"{mode} Mode {'⭐ ACTIVE' if is_active else ''}")

    col1, col2, col3 = st.columns(3)

    col1.metric("Range Low", f"${mode_range.get('range_low', '—')}")
    col2.metric("Range High", f"${mode_range.get('range_high', '—')}")
    col3.metric("Width (%)", f"{mode_range.get('width_pct', '—')}")

    st.write(
        f"**Liquidity Allocation:** {int(mode_alloc * 100)}% | "
        f"**Liquidity Floor:** "
        f"{int(mode_range.get('liquidity_floor', 0) * 100)}%"
    )

    if is_active:
        st.success("This mode is currently ACTIVE")

    st.divider()

# =================================================
# SECTION 5 — TECHNICAL DRIVERS
# =================================================
st.markdown("## 🧮 Technical Drivers")

ta_drivers = fusion_output.get("ta_drivers", [])

if ta_drivers:
    for driver in ta_drivers:
        st.write(f"• {driver}")
else:
    st.info("No strong technical drivers detected.")

# =================================================
# FOOTNOTE
# =================================================
st.caption(
    "ℹ️ Strategy mode is selected automatically. "
    "Manual override will be added in a later step."
)
