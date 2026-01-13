import streamlit as st

# -----------------------------
# SAFE IMPORTS
# -----------------------------
try:
    from data.store.price_store import get_current_price, get_price_history
    from core.strategy.fusion_engine import fuse_signals
except Exception as e:
    st.error(f"Critical import failure: {e}")
    st.stop()

# -----------------------------
# APP CONFIG
# -----------------------------
st.set_page_config(
    page_title="DeFiTuna LP Dashboard",
    layout="wide"
)

st.title("DeFiTuna LP Dashboard")
st.caption("Multi-Range Liquidity Intelligence System")

# -----------------------------
# SYMBOL CONFIG
# -----------------------------
symbol = "SOL"

# -----------------------------
# PRICE LAYER (SAFE)
# -----------------------------
try:
    current_price = get_current_price(symbol)
    price_history = get_price_history(symbol, days=60)  # 60 days REQUIRED for TA
except Exception as e:
    st.error(f"Price data unavailable: {e}")
    st.stop()

# -----------------------------
# DISPLAY PRICE
# -----------------------------
st.subheader("SOL Price")
st.metric("Current Price", f"${current_price:.2f}")

# -----------------------------
# FUSION ENGINE
# -----------------------------
try:
    fusion_output = fuse_signals(price_history)
except Exception as e:
    st.error(f"Strategy engine failed: {e}")
    st.stop()

# -----------------------------
# MARKET STATE
# -----------------------------
st.subheader("Market State")
c1, c2, c3 = st.columns(3)

c1.write("Direction")
c1.write(fusion_output.get("direction", "Unavailable"))

c2.write("Regime")
c2.write(fusion_output.get("regime", "Unavailable"))

c3.write("Confidence")
c3.write(round(fusion_output.get("confidence", 0.0), 2))

# -----------------------------
# ACTIVE STRATEGY
# -----------------------------
st.subheader("Active LP Strategy")

strategy = fusion_output.get("strategy", {})

st.write("Mode:", strategy.get("mode", "Unavailable"))
st.write("Capital Allocation (%):", strategy.get("capital_pct", 0))
st.write("Liquidity Floor (%):", strategy.get("liquidity_floor_pct", 0))

st.info(fusion_output.get("active_reason", "Strategy engine not active"))

# -----------------------------
# LIQUIDITY RANGES
# -----------------------------
st.subheader("Liquidity Ranges (All Modes)")

ranges = fusion_output.get("ranges", [])
if not ranges:
    st.warning("Range engine not active yet.")
else:
    for r in ranges:
        st.write(r)

# -----------------------------
# TECHNICAL ANALYSIS
# -----------------------------
st.subheader("Technical Analysis")

ta = fusion_output.get("ta_summary", {})

c1, c2, c3 = st.columns(3)
c1.metric("TA Score", ta.get("score", 0))
c2.metric("Volatility Regime", ta.get("volatility_regime", "Unavailable"))
c3.metric("Trend Strength", ta.get("trend_strength", "Unavailable"))

# -----------------------------
# TECHNICAL DRIVERS
# -----------------------------
st.subheader("Technical Drivers")

drivers = fusion_output.get("ta_drivers", [])
if not drivers:
    st.write("No technical drivers available.")
else:
    for d in drivers:
        st.write(f"• {d}")
