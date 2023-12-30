import requests
from datetime import datetime
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
def get_index_price(currency='ETH'):
    url = f"https://www.deribit.com/api/v2/public/get_index?currency={currency}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to retrieve index price from Deribit")
    return response.json()['result'][currency]

# Function to save data to PostgreSQL database
def save_to_db(df, engine, table='futures_data'):
    df.to_sql(table, engine, if_exists='append', index=False)

# Main function to process ETH futures and save data
def process_futures(engine):
    futures_data = get_futures(currency='ETH')
    index_price = get_index_price(currency='ETH')
    records = []
    for future in futures_data['result']:
        order_book = get_book(instrument=future['instrument_name'], depth=5)
        order_book = get_book(instrument='ETH-5JAN24', depth=5)
        spot_book = get_book(instrument='ETH_USDC', depth=5)
        best_ask_spot = spot_book['result']['best_ask_price'] 
        best_bid_spot = spot_book['result']['best_bid_price']
        best_ask_fut = order_book['result']['best_ask_price']
        best_bid_fut = order_book['result']['best_bid_price']
        ask_sizes_fut = sum([ask[1] for ask in order_book['result']['asks'][:5]])
        bid_sizes_fut = sum([bid[1] for bid in order_book['result']['bids'][:5]])
        ask_sizes_spot = sum([ask[1] for ask in order_book['result']['asks'][:5]])
        bid_sizes_spot = sum([bid[1] for bid in spot_book['result']['bids'][:5]])
        market_delta_fut = ask_sizes_fut - bid_sizes_fut
        market_delta_spot = ask_sizes_spot - bid_sizes_spot
        open_interest = order_book['result']['open_interest']
        volume_fut = order_book['result']['stats']['volume']
        volume_spot = spot_book['result']['stats']['volume']
        midpoint = (best_bid_fut + best_ask_fut) / 2
        entry_carry = best_bid_fut - best_ask_spot
        exit_carry = -best_ask_fut + best_bid_spot
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
            "best_bid_fut": best_bid_fut,
            "best_ask_fut": best_ask_fut,
            "midpoint": midpoint,
            "ask_sizes_fut": ask_sizes_fut,
            "bid_sizes_fut": bid_sizes_fut,
            "market_delta_fut": market_delta_fut,
            "open_interest": open_interest,
            "volume_fut": volume_fut,
            "spot": 'ETH_USDC',
            "best_bid_spot": best_bid_spot,
            "best_ask_spot": best_ask_spot, 
            "ask_sizes_spot": ask_sizes_spot,
            "bid_sizes_spot": bid_sizes_spot,
            "market_delta_spot": market_delta_spot,
            "volume_spot": volume_spot,
            "entry_carry": entry_carry,
            "exit_carry": exit_carry,
            "days_until_expiration": days_until_expiration,
            "index_difference": index_difference,
            "index_price": index_price,
            "percentage_difference": percentage_difference,
            "annualized_percentage_diff": annualized_percentage_diff
        })
        #print(f"Future: {future['instrument_name']}", "Annualized", f"{annualized_percentage_diff:.2f}%")
    df = pd.DataFrame(records)
    print(df)
    #save_to_db(df, engine)
    
db_params = "postgresql://postgres:example@postgres:5432/mydb"

engine = create_engine(db_params)

process_futures(engine)

'''
if __name__ == "__main__":
    while True:
        process_futures(engine, args.currency, args.spot, args.depth)
        time.sleep(1)

'''