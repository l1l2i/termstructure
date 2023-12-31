import requests
from datetime import datetime
import time
import pandas as pd
from sqlalchemy import create_engine

# Function to get the order book for a given instrument
def get_book(depth=10, instrument='ETH-PERPETUAL'):
    response = requests.get(f"https://deribit.com/api/v2/public/get_order_book?depth={depth}&instrument_name={instrument}")
    return response.json()


def get_futures(currency='ETH'):
    # Corrected by adding 'f' to make it an f-string for variable interpolation
    response = requests.get(f"https://www.deribit.com/api/v2/public/get_instruments?currency={currency}&kind=future&expired=false")
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
    futures_data = get_futures(currency='ETH')
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
        percentage_difference = ((midpoint - index_price) / index_price) * 100
        if days_until_expiration > 0:
            annualized_percentage_diff = percentage_difference * (365 / days_until_expiration)
        else:
            annualized_percentage_diff = 0  # To handle contracts that might have already expired or error in data
        current_timestamp = datetime.now()
        records.append({
            "timestamp": current_timestamp,
            "future": future['instrument_name'],
            "midpoint": midpoint,
            "days_until_expiration": days_until_expiration,
            "index_difference": index_difference,
            "index_price": index_price,
            "percentage_difference": percentage_difference,
            "annualized_percentage_diff": annualized_percentage_diff
        })
        print(f"Future: {future['instrument_name']}", "Annualized", f"{annualized_percentage_diff:.2f}%")
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
