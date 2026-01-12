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
# PRICE
# =================================================
st.markdown("## 🔵 Solana (SOL) Price")
st.metric("Current Price", f"${current_price:,.2f}")

# =================================================
# MARKET STATE
# =================================================
st.markdown("## 📈 Market State")
st.write(f"**Direction:** {fusion_output.get('final_direction', 'N/A')}")
st.write(f"**Regime:** {fusion_output.get('risk_mode', 'N/A')}")
st.write(f"**Confidence:** {fusion_output.get('final_confidence', 0.0)}")

# =================================================
# ACTIVE STRATEGY
# =================================================
st.markdown("## ⭐ Active LP Strategy")

active_mode = fusion_output.get("active_mode", "N/A")
active_range = fusion_output.get("active_range", {})
active_allocation = fusion_output.get("active_allocation", 0.0)

col1, col2, col3 = st.columns(3)

col1.metric("Active Mode", active_mode)
col2.metric("Range Low", f"${active_range.get('range_low', '—')}")
col3.metric("Range High", f"${active_range.get('range_high', '—')}")

st.write(f"**Capital Allocation:** {int(active_allocation * 100)}%")

st.divider()

# =================================================
# TECHNICAL DRIVERS
# =================================================
st.markdown("## 🧮 Technical Drivers")

ta_drivers = fusion_output.get("ta_drivers", [])

if ta_drivers:
    for driver in ta_drivers:
        st.write(f"• {driver}")
else:
    st.info("No strong technical drivers detected.")

# =================================================
# FUNDAMENTAL DRIVERS (SAFE)
# =================================================
st.markdown("## 🧠 Fundamental Drivers")

st.write(f"**FA Score:** {fusion_output.get('fa_score', 0.0)}")

fa_drivers = fusion_output.get("fa_drivers", [])

if fa_drivers:
    for driver in fa_drivers:
        st.write(f"• {driver}")
else:
    st.info("No fundamental drivers detected.")

# =================================================
# NEWS FEED (SAFE)
# =================================================
st.markdown("## 📰 News")

fa_news = fusion_output.get("fa_news", [])

if fa_news:
    for item in fa_news:
        title = item.get("title", "News")
        link = item.get("link", "#")
        st.markdown(f"- [{title}]({link})")
else:
    st.info("No major news items available.")

# =================================================
# FOOTNOTE
# =================================================
st.caption(
    "ℹ️ LP mode is selected automatically based on confidence, volatility, and regime."
)
