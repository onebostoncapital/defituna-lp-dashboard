import sys
import os
import streamlit as st

# =====================================================
# FIX: Ensure project root is on Python path
# =====================================================
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# =====================================================
# Imports (NOW SAFE)
# =====================================================
try:
    from data.store.price_store import get_current_price, get_price_history
except Exception as e:
    st.error(f"Price layer import failed: {e}")
    st.stop()

try:
    from core.strategy.fusion_engine import fuse_signals
except Exception as e:
    st.error(f"Strategy engine import failed: {e}")
    st.stop()

# =====================================================
# Page Config
# =====================================================
st.set_page_config(
    page_title="DeFiTuna LP Dashboard",
    layout="wide"
)

st.title("DeFiTuna LP Dashboard")
st.caption("Multi-Range Liquidity Intelligence System")

# =====================================================
# Symbol Config
# =====================================================
symbol = "SOL"

# =====================================================
# PRICE LAYER
# =====================================================
try:
    current_price = get_current_price(symbol)
    price_history = get_price_history(symbol, days=7)
except Exception as e:
    st.error("Price data unavailable.")
    st.exception(e)
    st.stop()

# =====================================================
# PRICE DISPLAY
# =====================================================
st.subheader("SOL Price")
st.metric("Current Price", f"${current_price:,.2f}")

# =====================================================
# STRATEGY ENGINE
# =====================================================
try:
    fusion_output = fuse_signals(price_history)
except Exception as e:
    st.error("Strategy engine failed")
    st.exception(e)
    st.stop()

# =====================================================
# NORMALIZATION (CRITICAL UI SAFETY)
# =====================================================
direction = fusion_output.get("direction", "Unavailable")
regime = fusion_output.get("regime", "Unavailable")
confidence = fusion_output.get("confidence", 0.0)

strategy = fusion_output.get("strategy")
if isinstance(strategy, str):
    strategy = {
        "mode": strategy,
        "capital_allocation_pct": 0,
        "liquidity_floor_pct": 0,
        "reason": "Default strategy fallback"
    }
elif strategy is None:
    strategy = {
        "mode": "Unavailable",
        "capital_allocation_pct": 0,
        "liquidity_floor_pct": 0,
        "reason": "Strategy engine not active"
    }

ta = fusion_output.get("ta", {})
ta_score = ta.get("score", 0)
ta_drivers = ta.get("drivers", [])

# =====================================================
# MARKET STATE
# =====================================================
st.subheader("Market State")
c1, c2, c3 = st.columns(3)
c1.metric("Direction", direction)
c2.metric("Regime", regime)
c3.metric("Confidence", round(confidence, 2))

# =====================================================
# ACTIVE LP STRATEGY
# =====================================================
st.subheader("Active LP Strategy")
st.write("Mode:", strategy.get("mode", "Unavailable"))
st.write("Capital Allocation (%):", strategy.get("capital_allocation_pct", 0))
st.write("Liquidity Floor (%):", strategy.get("liquidity_floor_pct", 0))
st.info(strategy.get("reason", ""))

# =====================================================
# LIQUIDITY RANGES
# =====================================================
st.subheader("Liquidity Ranges (All Modes)")
st.warning("Range engine not active yet.")

# =====================================================
# TECHNICAL ANALYSIS
# =====================================================
st.subheader("Technical Analysis")
c1, c2, c3 = st.columns(3)
c1.metric("TA Score", ta_score)
c2.metric("Volatility Regime", ta.get("volatility_regime", "Unavailable"))
c3.metric("Trend Strength", ta.get("trend_strength", "Unavailable"))

# =====================================================
# TECHNICAL DRIVERS
# =====================================================
st.subheader("Technical Drivers")
if ta_drivers:
    for d in ta_drivers:
        st.write(f"• {d}")
else:
    st.caption("No technical drivers available.")
