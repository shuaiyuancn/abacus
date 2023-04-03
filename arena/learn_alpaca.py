# %%
import os

from alpaca.data import StockHistoricalDataClient, StockLatestQuoteRequest

# %%
ALPACA_KEY = os.environ.get("ALPACA_KEY")
ALPACA_SECRET = os.environ.get("ALPACA_SECRET")

stock_client = StockHistoricalDataClient(ALPACA_KEY, ALPACA_SECRET)

# %%
request_params = StockLatestQuoteRequest(symbol_or_symbols="AAPL")

aapl = stock_client.get_stock_latest_quote(request_params)

# %%
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

from datetime import datetime

# %%
request_params = StockBarsRequest(
    symbol_or_symbols="AAPL",
    timeframe=TimeFrame.Day,
    start=datetime(2020, 1, 1),
    end=datetime(2020, 12, 31),
)

aapl_bars = stock_client.get_stock_bars(request_params)

# %%
