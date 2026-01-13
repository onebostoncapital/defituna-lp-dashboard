import streamlit as st

from data.store.price_store import (
    get_current_price,
    get_price_history
)

from core.strategy.fusion_engine import fuse_signals


# -----------------------------
# App Config
# -----------------------------
st.set_page_config(
    page_title="DeFiTuna LP Dashboard",
    layout="wide"
)

st.title("DeFiTuna LP Dashboard")
st.caption("Multi-Range Liquidity Intelligence System")


# -----------------------------
# Asset Selection (SAFE)
# -----------------------------
# Canonical symbol is handled by price layer
symbol = "SOL"


# -----------------------------
# Price Layer
# -----------------------------
try:
    current_price = get_current_price(symbol)
    price_history = get_price_history(symbol, days=7)

    st.subheader("SOL Price")
    st.metric("Current Price", f"${current_price:,.2f}")

except Exception as e:
    st.error("Price data unavailable.")
    st.stop()


# -----------------------------
# Strategy Fusion Engine
# -----------------------------
try:
    fusion_output = fuse_signals(price_history)
except Exception as e:
    st.error("Strategy engine failed.")
    st.exception(e)
    st.stop()


# -----------------------------
# Market State
# -----------------------------
st.subheader("Market State")

col1, col2, col3 = st.columns(3)

col1.write("**Direction**")
col1.write(fusion_output.get("direction", "Unavailable"))

col2.write("**Regime**")
col2.write(fusion_output.get("regime", "Unavailable"))

col3.write("**Confidence**")
col3.write(round(fusion_output.get("confidence", 0.0), 2))


# -----------------------------
# Active LP Strategy
# -----------------------------
st.subheader("Active LP Strategy")

strategy = fusion_output.get("active_strategy", {})

col1, col2 = st.columns(2)

col1.write("**Mode**")
col1.write(strategy.get("mode", "Unavailable"))

col2.write("**Capital Allocation (%)**")
col2.write(strategy.get("capital_allocation_pct", 0))


st.write("**Liquidity Floor (%)**")
st.write(strategy.get("liquidity_floor_pct", 0))


reason = fusion_output.get("active_reason")
if reason:
    st.info(reason)


# -----------------------------
# Liquidity Ranges
# -----------------------------
st.subheader("Liquidity Ranges (All Modes)")

ranges = fusion_output.get("multi_ranges", [])

if not ranges:
    st.warning("Range engine not active yet.")
else:
    for r in ranges:
        st.markdown(
            f"""
            **{r['mode']}**
            - Range Low: ${r['range_low']:.2f}
            - Range High: ${r['range_high']:.2f}
            - Width (%): {r['width_pct']}
            """
        )


# -----------------------------
# Technical Analysis Summary
# -----------------------------
st.subheader("Technical Analysis")

ta = fusion_output.get("ta_summary", {})

st.write("**TA Score**")
st.write(ta.get("score", 0))

st.write("**Volatility Regime**")
st.write(ta.get("volatility_regime", "Unavailable"))

st.write("**Trend Strength**")
st.write(ta.get("trend_strength", "Unavailable"))


# -----------------------------
# Technical Drivers
# -----------------------------
st.subheader("Technical Drivers")

drivers = fusion_output.get("ta_drivers", [])

if not drivers:
    st.write("No technical drivers available.")
else:
    for d in drivers:
        st.write(f"- {d}")
