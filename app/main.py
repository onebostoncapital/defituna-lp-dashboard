import streamlit as st

from data.store.price_store import (
    get_current_price,
    get_price_history
)

from core.strategy.fusion_engine import fuse_signals

# =============================
# APP CONFIG
# =============================

st.set_page_config(
    page_title="DeFiTuna LP Dashboard",
    layout="wide"
)

st.title("DeFiTuna LP Dashboard")
st.caption("Multi-Range Liquidity Intelligence System")

# =============================
# PRICE DATA
# =============================

price = get_current_price()

if price is None:
    st.error("Price data unavailable.")
    st.stop()

st.subheader("SOL Price")
st.metric("Current Price", f"${price:,.2f}")

price_history = get_price_history(days=7)

if price_history.empty:
    st.error("Historical price data unavailable.")
    st.stop()

# =============================
# STRATEGY ENGINE
# =============================

fusion_output = fuse_signals(price_history)

# =============================
# MARKET STATE
# =============================

st.subheader("Market State")

c1, c2, c3 = st.columns(3)

c1.metric("Direction", fusion_output.get("direction", "N/A"))
c2.metric("Regime", fusion_output.get("regime", "Unavailable"))
c3.metric("Confidence", fusion_output.get("confidence", 0.0))

# =============================
# ACTIVE STRATEGY
# =============================

st.subheader("Active LP Strategy")

st.write("Mode:", fusion_output.get("active_mode", "Defensive"))
st.write("Capital Allocation (%):", fusion_output.get("capital_allocation", 0))
st.write("Liquidity Floor (%):", fusion_output.get("liquidity_floor", 0))

reason = fusion_output.get("active_reason")
if reason:
    st.info(reason)

# =============================
# LIQUIDITY RANGES
# =============================

st.subheader("Liquidity Ranges (All Modes)")

ranges = fusion_output.get("ranges")

if not ranges:
    st.warning("Range engine not active yet.")
else:
    for mode, r in ranges.items():
        st.markdown(f"**{mode}**")
        st.write(
            f"Low: ${r['low']:.2f} | High: ${r['high']:.2f} | Width: {r['width_pct']:.1f}%"
        )

# =============================
# TECHNICAL ANALYSIS
# =============================

st.subheader("Technical Analysis")

st.metric("TA Score", fusion_output.get("ta_score", 0))
st.write("Volatility Regime:", fusion_output.get("volatility_regime", "Unavailable"))
st.write("Trend Strength:", fusion_output.get("trend_strength", "Unavailable"))

# =============================
# TECHNICAL DRIVERS
# =============================

st.subheader("Technical Drivers")

drivers = fusion_output.get("ta_drivers", [])

if not drivers:
    st.info("No technical drivers available.")
else:
    for d in drivers:
        st.write("•", d)
