import streamlit as st

from data.store.price_store import (
    get_current_price,
    get_price_history
)

from core.strategy.fusion_engine import fuse_signals


# -----------------------------
# Streamlit Config
# -----------------------------
st.set_page_config(
    page_title="DeFiTuna LP Dashboard",
    layout="wide"
)

st.title("DeFiTuna LP Dashboard")
st.caption("Multi-Range Liquidity Intelligence System")


# -----------------------------
# Asset
# -----------------------------
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
    st.error("Price data unavailable")
    st.exception(e)
    st.stop()


# -----------------------------
# Fusion Engine
# -----------------------------
try:
    fusion_output = fuse_signals(price_history)
except Exception as e:
    st.error("Strategy engine failed")
    st.exception(e)
    st.stop()


# -----------------------------
# Market State
# -----------------------------
st.subheader("Market State")

c1, c2, c3 = st.columns(3)

c1.metric("Direction", fusion_output.get("direction", "Unavailable"))
c2.metric("Regime", fusion_output.get("regime", "Unavailable"))
c3.metric("Confidence", round(fusion_output.get("confidence", 0.0), 2))


# -----------------------------
# Active Strategy
# -----------------------------
st.subheader("Active LP Strategy")

strategy = fusion_output.get("active_strategy", {})

st.write("**Mode**:", strategy.get("mode", "Unavailable"))
st.write("**Capital Allocation (%)**:", strategy.get("capital_allocation_pct", 0))
st.write("**Liquidity Floor (%)**:", strategy.get("liquidity_floor_pct", 0))

if fusion_output.get("active_reason"):
    st.info(fusion_output["active_reason"])


# -----------------------------
# Liquidity Ranges
# -----------------------------
st.subheader("Liquidity Ranges")

ranges = fusion_output.get("multi_ranges", [])

if not ranges:
    st.warning("Range engine not active yet")
else:
    for r in ranges:
        st.markdown(
            f"""
            **{r['mode']}**
            - Low: ${r['range_low']:.2f}
            - High: ${r['range_high']:.2f}
            - Width (%): {r['width_pct']}
            """
        )


# -----------------------------
# Technical Drivers
# -----------------------------
st.subheader("Technical Drivers")

drivers = fusion_output.get("ta_drivers", [])

if drivers:
    for d in drivers:
        st.write(f"- {d}")
else:
    st.write("No technical drivers available")
