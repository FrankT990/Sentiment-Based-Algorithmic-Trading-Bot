import os
import Alpaca_Trader as AT
import json
import Sent_Analyzer as SA

with open("config.json") as f:
    keys = json.load(f)
os.environ.update(keys)

finnhub_key = os.environ.get('FINNHUB_KEY')
api_key = os.environ.get('ALPACA_API_KEY')
alpaca_secret_key = os.environ.get('ALPACA_SECRET_KEY')


ticker = 'AAPL'
client = AT.TradingClient(api_key, alpaca_secret_key, paper=True, url_override=None)
current_orders = AT.get_active_orders(ticker, client)
positions = AT.get_positions(client)
print(positions)
print(type(positions))
print(type(current_orders))

