import requests
from datetime import datetime
import time
import pandas as pd
from sqlalchemy import create_engine

# Function to get the order book for a given instrument
def get_book(depth=10, instrument='ETH-PERPETUAL'):
    response = requests.get(f"https://test.deribit.com/api/v2/public/get_order_book?depth={depth}&instrument_name={instrument}")
    return response.json()

# Function to get ETH futures data from Deribit
def get_eth_futures():
    url = "https://www.deribit.com/api/v2/public/get_instruments?currency=ETH&kind=future&expired=false"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to retrieve data from Deribit")
    return response.json()

# Function to get ETH index price
def get_eth_index_price():
    url = "https://www.deribit.com/api/v2/public/get_index?currency=ETH"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to retrieve ETH index price from Deribit")
    return response.json()['result']['ETH']

# Function to save data to PostgreSQL database
def save_to_db(df, engine):
    df.to_sql('eth_futures_data', engine, if_exists='append', index=False)

# Main function to process ETH futures and save data
def process_eth_futures(engine):
    futures_data = get_eth_futures()
    index_price = get_eth_index_price()
    records = []
    for future in futures_data['result']:
        order_book = get_book(instrument=future['instrument_name'])
        best_bid = order_book['result']['best_bid_price']
        best_ask = order_book['result']['best_ask_price']
        midpoint = (best_bid + best_ask) / 2
        expiration_timestamp = future['expiration_timestamp'] / 1000
        days_until_expiration = (expiration_timestamp - datetime.now().timestamp()) / (60 * 60 * 24)
        index_difference = midpoint - index_price
        current_timestamp = datetime.now()
        records.append({
            "timestamp": current_timestamp,
            "future": future['instrument_name'],
            "midpoint": midpoint,
            "days_until_expiration": days_until_expiration,
            "index_difference": index_difference,
            "index_price": index_price
        })
    df = pd.DataFrame(records)
    save_to_db(df, engine)

# Setup database connection parameters
db_params = "postgresql://postgres:example@postgres:5432/mydb"

# Setup database engine
engine = create_engine(db_params)

# Continuous data collection every second
while True:
    process_eth_futures(engine)
    time.sleep(1)
