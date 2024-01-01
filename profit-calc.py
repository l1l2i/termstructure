import requests
from datetime import datetime
import pandas as pd
#from sqlalchemy import create_engine

DEPTH = 10
SPOT = 'BTC_USDC'


# Function to get the order book for a given instrument
def get_book(depth=10, instrument='ETH-PERPETUAL'):
    response = requests.get(f"https://deribit.com/api/v2/public/get_order_book?depth={depth}&instrument_name={instrument}")
    return response.json()

#order_book = get_book(instrument='ETH-5JAN24', depth=5)

fut1 = get_book(instrument='ETH-5JAN24', depth=5)
fut2 = get_book(instrument='ETH-5JAN24', depth=5)

spot = get_book(instrument=SPOT, depth=DEPTH)

best_ask_spot = spot_book['result']['best_ask_price'] 
best_bid_spot = spot_book['result']['best_bid_price']
best_ask_fut = order_book['result']['best_ask_price']
best_bid_fut = order_book['result']['best_bid_price']




# Data Set
#prices = [42710, 42686.54, 42725.40, 42800, 42799.93]
#volumes = [0.5, 1, 1, 1, 1]

# Calculating Volume Weighted Average Price (VWAP)
#vwap = sum(p*v for p, v in zip(prices, volumes)) / sum(volumes)
#vwap

# 42748.19333333333


# futures orders 

# BTC-26JAN24 43335 -2.461763589803018 -108340
# BTC-23FEB24 43858.99 -1.9691819435709104  -87760
