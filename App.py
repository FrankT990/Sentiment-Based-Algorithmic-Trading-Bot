import streamlit as st
import Alpaca_Trader
import Sent_Analyzer
import Login_Page
import Trading
import os
import json

with open("config.json") as f:
    keys = json.load(f)
os.environ.update(keys)

st.session_state['finnhub_key'] = os.environ.get('FINNHUB_KEY')
st.session_state['alpaca_key'] = os.environ.get('ALPACA_API_KEY')
st.session_state['alpaca_secret'] = os.environ.get('ALPACA_SECRET_KEY')

if st.session_state["alpaca_key"] is None or st.session_state["alpaca_secret"] is None or st.session_state["finnhub_key"] is None:
  Login_Page.get_api_keys()
elif "ticker" not in st.session_state:
  Trading.get_ticker()
else:
  Trading.run_trades()
