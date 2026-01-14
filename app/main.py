import sys
import os

# -----------------------
# BOOTSTRAP PROJECT ROOT
# -----------------------
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st

from data.store.price_store import get_current_price, get_price_history
from core.ta.ta_aggregator import aggregate_ta_signals
from core.market_state.market_state_engine import derive_market_state

st.set_page_config(layout="wide")

st.title("DeFiTuna LP Dashboard")
st.caption("Multi-Range Liquidity Intelligence System")

symbol = "SOL"

# -----------------------
# PRICE
# -----------------------
current_price = get_current_price(symbol)
st.subheader("SOL Price")
st.metric("Current Price", f"${current_price:.2f}")

# -----------------------
# TECHNICAL ANALYSIS (PHASE 1)
# -----------------------
price_history = get_price_history(symbol, days=30)
ta_output = aggregate_ta_signals(price_history)

# -----------------------
# MARKET STATE (PHASE 2)
# -----------------------
market_state = derive_market_state(ta_output)

st.subheader("Market State")
c1, c2, c3 = st.columns(3)

c1.metric("Direction", market_state["direction"])
c2.metric("Regime", market_state["regime"])
c3.metric("Confidence", market_state["confidence"])

# -----------------------
# TA DETAILS
# -----------------------
st.subheader("Technical Analysis")

st.write("TA Score:", ta_output["ta_score"])
st.write("Volatility Regime:", ta_output["volatility"])
st.write("Trend Strength:", ta_output["trend"])

st.subheader("Technical Drivers")
if ta_output["drivers"]:
    for d in ta_output["drivers"]:
        st.write("•", d)
else:
    st.caption("No technical drivers available.")
