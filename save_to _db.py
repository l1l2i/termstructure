import requests
from datetime import datetime
import time
import psycopg2

# Database connection parameters
db_params = {
    "dbname": "your_dbname",
    "user": "your_username",
    "password": "your_password",
    "host": "your_host",
    "port": "your_port"
}

# Function definitions (get_book, get_eth_futures, get_eth_index_price) remain the same

def save_to_db(data):
    with psycopg2.connect(**db_params) as conn:
        with conn.cursor() as cursor:
            query = """
            INSERT INTO eth_futures_data (timestamp, future, midpoint, days_until_expiration, index_difference, index_price)
            VALUES (%s, %s, %s, %s, %s, %s);
            """
            cursor.execute(query, data)

def process_eth_futures():
    futures_data = get_eth_futures()
    index_price = get_eth_index_price()

    for future in futures_data['result']:
        order_book = get_book(instrument=future['instrument_name'])
        best_bid = order_book['result']['best_bid_price']
        best_ask = order_book['result']['best_ask_price']
        midpoint = (best_bid + best_ask) / 2

        expiration_timestamp = future['expiration_timestamp'] / 1000
        days_until_expiration = (expiration_timestamp - datetime.now().timestamp()) / (60 * 60 * 24)

        index_difference = midpoint - index_price

        current_timestamp = datetime.now()

        # Save data to database
        save_to_db((current_timestamp, future['instrument_name'], midpoint, days_until_expiration, index_difference, index_price))

# Run the script to collect data every second
while True:
    process_eth_futures()
    time.sleep(1)
