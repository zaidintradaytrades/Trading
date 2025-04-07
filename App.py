import streamlit as st
from trade_signal import scan_market

st.set_page_config(page_title="Trade Signals", layout="wide")

st.title("Intraday Trade Signal Scanner")
st.markdown("Scans NSE 500 stocks every hour using breakout and volume logic.")

if st.button("Run Live Scan"):
    result = scan_market()
    if result:
        st.success("Signal Found!")
        st.write(result)
    else:
        st.warning("No qualified stock right now.")
