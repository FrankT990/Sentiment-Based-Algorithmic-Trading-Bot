import streamlit as st

def get_api_keys():
  st.markdown("<h1 style='text-align: center;'>News Sentiment Algorithmic Trading Bot</h1>", unsafe_allow_html=True)
  st.markdown("<h3 style='text-align: center;'>Frank Tittiger</h3>", unsafe_allow_html=True)
  st.subheader("Enter API keys below")
  finnhub_key = st.text_input("Enter your Finnhub API key:", type="password")
  alpaca_key = st.text_input("Enter your Alpaca API key:", type="password")
  alpaca_secret = st.text_input("Enter your Alpaca Secret key:", type="password")
  if st.button("Submit Keys and Continue"):
    if finnhub_key and alpaca_key and alpaca_secret:
        st.session_state['finnhub_key'] = finnhub_key
        st.session_state['alpaca_key'] = alpaca_key
        st.session_state['alpaca_secret'] = alpaca_secret
        st.session_state['logged_in'] = True
        st.session_state['logged_in'] = True
        st.rerun()
        st.success("API keys saved successfully!")      
    else:
        st.error("Please enter all three API keys to proceed.")
