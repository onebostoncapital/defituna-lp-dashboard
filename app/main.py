# =================================================
# STREAMLIT CLOUD IMPORT FIX (MUST BE FIRST)
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
from core.fa.fa_aggregator import aggregate_fa_signals

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
# DATA FETCH (PRICE STORE)
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
fa_output = aggregate_fa_signals()

# =================================================
# SECTION 1 — PRICE
# =================================================
st.markdown("## 🔵 Solana (SOL) Price")
st.metric("Current Price", f"${current_price:,.2f}")

# =================================================
# SECTION 2 — MARKET STATE
# =================================================
st.markdown("## 📈 Market State")
st.write(f"**Direction:** {fusion_output.get('final_direction', 'N/A')}")
st.write(f"**Regime:** {fusion_output.get('risk_mode', 'N/A')}")
st.write(f"**Confidence:** {fusion_output.get('final_confidence', 0.0)}")

# =================================================
# SECTION 3 — ACTIVE STRATEGY
# =================================================
st.markdown("## ⭐ Active LP Strategy")

active_range = fusion_output.get("active_range", {})

col1, col2, col3, col4 = st.columns(4)

col1.metric("Mode", fusion_output.get("active_mode", "N/A"))
col2.metric("Range Low", f"${active_range.get('range_low', 0)}")
col3.metric("Range High", f"${active_range.get('range_high', 0)}")
col4.metric("Width (%)", active_range.get("width_pct", 0))

st.write(
    f"**Capital Allocation:** "
    f"{int(fusion_output.get('active_allocation', 0) * 100)}%"
)

st.info(
    fusion_output.get(
        "strategy_explanation",
        "Strategy selected automatically based on confidence, volatility, and regime."
    )
)

st.divider()

# =================================================
# SECTION 4 — MULTI-RANGE VIEW
# =================================================
st.markdown("## 🧩 Liquidity Ranges (All Modes)")

multi_ranges = fusion_output.get("multi_ranges", {})
ranges = multi_ranges.get("ranges", {})
allocation = multi_ranges.get("allocation", {})
active_mode = fusion_output.get("active_mode")

for mode in ["Defensive", "Balanced", "Aggressive"]:
    data = ranges.get(mode)
    if not data:
        continue

    is_active = mode == active_mode
    st.subheader(f"{mode} {'⭐ ACTIVE' if is_active else ''}")

    c1, c2, c3 = st.columns(3)
    c1.metric("Range Low", f"${data['range_low']}")
    c2.metric("Range High", f"${data['range_high']}")
    c3.metric("Width (%)", data["width_pct"])

    st.write(
        f"**Liquidity Allocation:** {int(allocation.get(mode, 0) * 100)}% "
        f"(Floor: {int(data['liquidity_floor'] * 100)}%)"
    )

    if is_active:
        st.success("This mode is currently ACTIVE")

    st.divider()

# =================================================
# SECTION 5 — TECHNICAL DRIVERS
# =================================================
st.markdown("## 🧮 Technical Drivers")
for driver in fusion_output.get("ta_drivers", []):
    st.write(f"• {driver}")

# =================================================
# SECTION 6 — FUNDAMENTAL NEWS (DYNAMIC & CLICKABLE)
# =================================================
st.markdown("## 📰 Live Fundamental News")

news_items = fa_output.get("news_items", [])

if not news_items:
    st.info("No live news available right now.")
else:
    # Show at least ONE live news item
    for item in news_items[:3]:
        st.markdown(
            f"- [{item['title']}]({item['url']})  \n"
            f"  _{item.get('source', 'Unknown source')}_"
        )

st.caption("News updates automatically on refresh.")

# =================================================
# FOOTNOTE
# =================================================
st.caption(
    "ℹ️ This dashboard auto-refreshes live data. "
    "News sources include crypto, macro, and geopolitical feeds."
)
