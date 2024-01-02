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

# Function to get the order book for a given instrument
def get_book(depth=10, instrument='ETH-PERPETUAL'):
    response = requests.get(f"https://deribit.com/api/v2/public/get_order_book?depth={depth}&instrument_name={instrument}")
    return response.json()

#order_book = get_book(instrument='ETH-5JAN24', depth=5)

fut1 = get_book(instrument='BTC-26JAN24', depth=5)
fut2 = get_book(instrument='BTC-23FEB24', depth=5)

spot = get_book(instrument=SPOT, depth=DEPTH)

best_ask_spot = spot['result']['best_ask_price'] 
best_bid_spot = spot['result']['best_bid_price']

best_ask_fut_1 = fut1['result']['best_ask_price']
best_bid_fut_1 = fut1['result']['best_bid_price']

best_ask_fut_2 = fut2['result']['best_ask_price']
best_bid_fut_2 = fut2['result']['best_bid_price']


Pair1_max_profit = Fut1_entry*Fut1_volume - Spot1_entry*Spot1_volume
Pair2_max_profit = Fut2_entry*Fut2_volume - Spot2_entry*Spot2_volume

PnL_fut_1 = (Fut1_usd/best_ask_fut_1-Fut1_usd/Fut1_entry)*best_ask_spot
PnL_spot_1 = (best_bid_spot - Spot1_entry)*Spot1_volume

Port_usd_1 = (Spot1_volume + (Fut1_usd/best_ask_fut_1-Fut1_usd/Fut1_entry))*best_bid_spot
PnL_1 = PnL_spot_1 + PnL_fut_1
CryptoBalance_1 = Spot1_volume + (Fut1_usd/best_ask_fut_1-Fut1_usd/Fut1_entry)

PnL_fut_2 = (Fut2_usd/best_ask_fut_2-Fut2_usd/Fut2_entry)*best_ask_spot
PnL_spot_2 = (best_bid_spot - Spot2_entry)*Spot2_volume

Port_usd_2 = (Spot2_volume + (Fut2_usd/best_ask_fut_2-Fut2_usd/Fut2_entry))*best_bid_spot
PnL_2 = PnL_spot_2 + PnL_fut_2
CryptoBalance_2 = Spot2_volume + (Fut2_usd/best_ask_fut_2-Fut2_usd/Fut2_entry)

Total_port_value_usd = Port_usd_1 + Port_usd_2
Total_PnL = PnL_1 + PnL_2
Total_BTC = CryptoBalance_1 + CryptoBalance_2



#4.5 + (Fut1_usd/best_ask_fut_1-Fut1_usd/Fut1_entry) + (Fut2_usd/best_ask_fut_2-Fut2_usd/Fut2_entry)
#(4.5 + (Fut1_usd/best_ask_fut_1-Fut1_usd/Fut1_entry) + (Fut2_usd/best_ask_fut_2-Fut2_usd/Fut2_entry))*best_bid_spot

print(f"PnL_fut_1: {PnL_fut_1}")
print(f"PnL_spot_1: {PnL_spot_1}")
print(f"Port_usd_1: {Port_usd_1}")
print(f"PnL_1: {PnL_1}")
print("-" * 30)
print(f"PnL_fut_2: {PnL_fut_2}")
print(f"PnL_spot_2: {PnL_spot_2}")
print(f"Port_usd_2: {Port_usd_2}")
print(f"PnL_2: {PnL_2}")
print("-" * 30)
print(f"Total_port_value_usd: {Total_port_value_usd}")
print(f"Total_PnL: {Total_PnL}")
print(f"Pair1_max_profit: {Pair1_max_profit}")
print(f"Pair2_max_profit: {Pair2_max_profit}")
print("-" * 30)
print(f"Total_port_value_usd: {Total_port_value_usd}")
print(f"Total_PnL: {Total_PnL}")
print("-" * 30)
print(f"Total_BTC: {Total_BTC}")
print(f"CryptoBalance_1: {CryptoBalance_1}")
print(f"CryptoBalance_2: {CryptoBalance_2}")

#market_profit = 
#liquidate_profit
#volume_to_roll



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