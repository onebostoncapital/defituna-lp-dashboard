# =================================================
# STREAMLIT PATH FIX (REQUIRED)
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
from core.scenario.scenario_engine import run_scenario_engine
from core.fa.news.crypto_news import fetch_crypto_news

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
# PRICE DATA
# =================================================
with st.spinner("Fetching SOL price data..."):
    current_price = get_current_price()
    price_history = get_price_history(days=200)

if current_price is None or price_history is None:
    st.error("Price data unavailable")
    st.stop()

# =================================================
# CORE ENGINE
# =================================================
fusion_output = fuse_signals(price_history)

# =================================================
# OPTION C — SCENARIO ENGINE
# =================================================
scenario_output = run_scenario_engine(
    fusion_output=fusion_output,
    capital_usd=10000,
    leverage=2,
    horizon_days=7
)

# =================================================
# PRICE
# =================================================
st.markdown("## 🔵 Solana (SOL) Price")
st.metric("Current Price", f"${current_price:,.2f}")

# =================================================
# MARKET STATE
# =================================================
st.markdown("## 📈 Market State")
st.write(f"**Direction:** {fusion_output['final_direction']}")
st.write(f"**Regime:** {fusion_output['risk_mode']}")
st.write(f"**Confidence:** {fusion_output['final_confidence']}")

# =================================================
# ACTIVE STRATEGY
# =================================================
st.markdown("## ⭐ Active LP Strategy")

col1, col2, col3 = st.columns(3)
col1.metric("Active Mode", fusion_output["active_mode"])
col2.metric("Range Low", f"${fusion_output['active_range']['range_low']}")
col3.metric("Range High", f"${fusion_output['active_range']['range_high']}")

st.info(fusion_output["active_reason"])
st.divider()

# =================================================
# MULTI-RANGE VIEW
# =================================================
st.markdown("## 🧩 Liquidity Ranges")

ranges = fusion_output["multi_ranges"]["ranges"]
allocation = fusion_output["multi_ranges"]["allocation"]

for mode in ["Defensive", "Balanced", "Aggressive"]:
    st.subheader(mode)

    col1, col2, col3 = st.columns(3)
    col1.metric("Range Low", f"${ranges[mode]['range_low']}")
    col2.metric("Range High", f"${ranges[mode]['range_high']}")
    col3.metric("Width (%)", ranges[mode]["width_pct"])

    st.write(
        f"Allocation: {int(allocation[mode] * 100)}% | "
        f"Floor: {int(ranges[mode]['liquidity_floor'] * 100)}%"
    )

    st.divider()

# =================================================
# OPTION C — CAPITAL SCENARIO
# =================================================
st.markdown("## 💰 Capital Scenario Intelligence (7-Day View)")

for mode, data in scenario_output.items():
    st.subheader(mode)

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Allocated USD", f"${data['allocated_usd']}")
    col2.metric("Liquidity Floor USD", f"${data['liquidity_floor_usd']}")
    col3.metric("Fees (24h)", f"${data['fees_24h']}")
    col4.metric("Fees (7d)", f"${data['fees_7d']}")
    col5.metric("Price Scenario", f"${data['price_appreciation']}")

    st.success(f"Net Scenario Outcome (7d): ${data['net_scenario']}")
    st.divider()

# =================================================
# TECHNICAL DRIVERS
# =================================================
st.markdown("## 🧮 Technical Drivers")
for d in fusion_output["ta_drivers"]:
    st.write(f"• {d}")

# =================================================
# FUNDAMENTAL DRIVERS
# =================================================
st.markdown("## 🌍 Fundamental Drivers")
for d in fusion_output["fa_drivers"]:
    st.write(f"• {d}")

# =================================================
# LIVE NEWS
# =================================================
st.markdown("## 📰 Live Crypto News")

news = fetch_crypto_news()
if news and news.get("items"):
    for item in news["items"][:3]:
        st.markdown(f"- [{item['title']}]({item['link']})")
else:
    st.write("No major crypto news right now.")

# =================================================
# FOOTNOTE
# =================================================
st.caption(
    "ℹ️ Scenario results are estimates, not predictions. "
    "Impermanent loss is intentionally excluded and will be "
    "handled during historical backtesting (OPTION D)."
)
