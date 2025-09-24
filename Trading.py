import streamlit as st
import Alpaca_Trader as AT
import Login_Page 
import requests
import time
import Sent_Analyzer as SA


def get_ticker():
  st.markdown("<h1 style='text-align: center;'>News Sentiment Algorithmic Trading Bot</h1>", unsafe_allow_html=True)
  st.markdown("<h3 style='text-align: center;'>Frank Tittiger</h3>", unsafe_allow_html=True)

  ticker = st.text_input("Enter Asset Ticker (ex: AAPL, MSFT, BTC, etc)").upper()
  client = AT.TradingClient(api_key=st.session_state['alpaca_key'], secret_key=st.session_state['alpaca_secret'], paper=True, url_override=None)
  
  if st.button("Continue"):
    req = AT.GetAssetsRequest(
    # asset_class=AssetClass.US_EQUITY,  # default asset_class is us_equity
    status=AT.AssetStatus.ACTIVE,
    exchange=AT.AssetExchange.NASDAQ,
    )
    assets = client.get_all_assets(req)

    assets = [asset.symbol for asset in assets]
    if ticker not in assets:
      st.error("Please enter a valid ticker to continue")
    else:
      st.session_state['ticker'] = ticker
      st.session_state['logged_in'] = True
      st.rerun()


def run_trades():
  st.markdown("<h1 style='text-align: center;'>News Sentiment Algorithmic Trading Bot</h1>", unsafe_allow_html=True)
  st.markdown("<h3 style='text-align: center;'>Frank Tittiger</h3>", unsafe_allow_html=True)

  client = AT.TradingClient(api_key=st.session_state['alpaca_key'], secret_key=st.session_state['alpaca_secret'], paper=True, url_override=None)
  st.write("Running trades for:", st.session_state['ticker'])

  headlines = SA.write_headlines(st.session_state['ticker'], SA.one_year_ago(), SA.date_now(), st.session_state['finnhub_key'])
  percent_changes = SA.write_performance_dict(st.session_state['ticker'])
  df = SA.make_data(percent_changes, headlines)
  [RFR_model, vectorizer, mse] = SA.make_model(df)

  empty = st.empty()
  while (True):
    with empty.container():
      current_orders = AT.get_active_orders(st.session_state['ticker'], client)
      current_positions = AT.get_positions(client)

      st.write("Acquiring headlines...")
      recent_headline = SA.get_most_recent_headline(st.session_state['ticker'], st.session_state['finnhub_key'])
      st.write("Recent headline acquired: " + recent_headline)
      pc = SA.predict_headline(RFR_model, vectorizer, recent_headline)
      if pc > 0:
        sentiment = " (positive sentiment)"
      else:
        sentiment = " (negative sentiment)"
      st.write("Estimated percent change: " + str(pc) + sentiment)

      if (len(current_orders) == 0):
        if (len(current_positions) == 0):
          if pc > 0:
            st.write("No current position open, submitting buy order")
            AT.submit_order_buy(st.session_state['ticker'], 1, client)
            st.lael("Buy order submitted")
            time.sleep(60)
          else:
            st.write("Negative sentiment detected, waiting for next headline")  
            time.sleep(60)        
        time.sleep(60)
      else:
        if (pc < 0):
          st.write("Negative sentiment detected and active position open, submitting sell order to close position")
          AT.submit_order_sell(st.session_state['ticker'], 1, client)
          st.write("Sell order submitted")
        time.sleep(60)