CREATE TABLE eth_futures_data (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    future VARCHAR(255) NOT NULL,
    midpoint DECIMAL NOT NULL,
    days_until_expiration DECIMAL NOT NULL,
    index_difference DECIMAL NOT NULL,
    index_price DECIMAL NOT NULL
);
