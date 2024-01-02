import requests
from datetime import datetime
import pandas as pd
#from sqlalchemy import create_engine

DEPTH = 10
SPOT = 'BTC_USDC'

Spot1_entry = 42706.78
Spot1_volume = 2.5
Fut1_entry = 43335
Fut1_volume = 2.5000576901
Fut1_usd = 108340

Spot2_entry = 42799.965
Spot2_volume = 2
Fut2_entry = 43859
Fut2_volume = 2.0009576141727
Fut2_usd = 87760

Pair1_max_profit = Fut1_entry*Fut1_volume - Spot1_entry*Spot1_volume
Pair2_max_profit = Fut2_entry*Fut2_volume - Spot2_entry*Spot2_volume


# Function to get the order book for a given instrument
def get_book(depth=10, instrument='ETH-PERPETUAL'):
    response = requests.get(f"https://deribit.com/api/v2/public/get_order_book?depth={depth}&instrument_name={instrument}")
    return response.json()

#order_book = get_book(instrument='ETH-5JAN24', depth=5)

fut1 = get_book(instrument='ETH-5JAN24', depth=5)
fut2 = get_book(instrument='ETH-5JAN24', depth=5)

spot = get_book(instrument=SPOT, depth=DEPTH)

best_ask_spot = spot['result']['best_ask_price'] 
best_bid_spot = spot['result']['best_bid_price']

best_ask_fut_1 = fut1['result']['best_ask_price']
best_bid_fut_1 = fut1['result']['best_bid_price']

best_ask_fut_2 = fut2['result']['best_ask_price']
best_bid_fut_2 = fut2['result']['best_bid_price']


PnL = 

market_profit = 
liquidate_profit
volume_to_roll



# Data Set
#prices = [42710, 42686.54, 42725.40, 42800, 42799.93]
#volumes = [0.5, 1, 1, 1, 1]

# Calculating Volume Weighted Average Price (VWAP)
#vwap = sum(p*v for p, v in zip(prices, volumes)) / sum(volumes)
#vwap

# 42748.19333333333 jan 


# futures orders 

# BTC-26JAN24 43335 -2.461763589803018 -108340
# BTC-23FEB24 43858.99 -1.9691819435709104  -87760


#JAN SPOT =  42706.78 / 2.5 FUT = 43335 / 2.5000576901
#FEB SPOT =  42799.965 /2 FUR = 43859 / 2.0009576141727