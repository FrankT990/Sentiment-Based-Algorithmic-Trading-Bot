import alpaca
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from alpaca.trading.client import TradingClient
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from alpaca.data.historical.corporate_actions import CorporateActionsClient
from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.trading.stream import TradingStream
from alpaca.data.live.stock import StockDataStream

from alpaca.data.requests import (
    CorporateActionsRequest,
    StockBarsRequest,
    StockQuotesRequest,
    StockTradesRequest,
)
from alpaca.trading.requests import (
    ClosePositionRequest,
    GetAssetsRequest,
    GetOrdersRequest,
    LimitOrderRequest,
    MarketOrderRequest,
    StopLimitOrderRequest,
    StopLossRequest,
    StopOrderRequest,
    TakeProfitRequest,
    TrailingStopOrderRequest,
)
from alpaca.trading.enums import (
    AssetExchange,
    AssetStatus,
    OrderClass,
    OrderSide,
    OrderType,
    QueryOrderStatus,
    TimeInForce,
)


def get_active_orders(tkr, client):
    try:
        req = GetOrdersRequest(
            status = QueryOrderStatus.OPEN,
            symbols = [tkr]
        )
        orders = client.get_orders(req)
        return orders
    except Exception as e:
        print('get_active_orders error:', e)
        raise

def get_positions(client):
    try:
        positions = client.get_all_positions()
        return positions
    except Exception as e:
        print('get_positions error:', e)
        raise

def submit_order_buy(tkr, qty, client):
    market_order_data = MarketOrderRequest(
                    symbol=tkr,
                    qty=qty,
                    side=OrderSide.BUY,
                    time_in_force=TimeInForce.DAY
                    )
    market_order = client.submit_order(
                order_data=market_order_data
    )
    return market_order

def submit_order_sell(tkr, qty, client):
    market_order_data = MarketOrderRequest(
                    symbol=tkr,
                    qty=qty,
                    side=OrderSide.SELL,
                    time_in_force=TimeInForce.DAY
                    )
    market_order = client.submit_order(
                order_data=market_order_data
    )
    return market_order