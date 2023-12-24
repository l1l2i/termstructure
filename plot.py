import plotly.graph_objects as go
from plotly.subplots import make_subplots
import psycopg2
import pandas as pd

# Database connection parameters
#db_params = "postgresql://your_username:your_password@your_host:your_port/your_dbname"
db_params = "postgresql://postgres:example@127.0.0.1:5432/mydb"

# Connect to the PostgreSQL database
conn = psycopg2.connect(db_params)

# Query to retrieve data
query = """
SELECT timestamp, future, index_price, annualized_percentage_diff
FROM eth_futures_data
WHERE future != 'ETH-PERPETUAL'
ORDER BY timestamp ASC;
"""

# Read data into a DataFrame
df = pd.read_sql(query, conn)

# Close the database connection
conn.close()

# Prepare the figure with subplots
fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                    vertical_spacing=0.1,
                    subplot_titles=('Index Price', 'Annualized Percentage Difference'))

# Add the index price time series to the main panel
fig.add_trace(
    go.Scatter(x=df['timestamp'], y=df['index_price'], name='Index Price'),
    row=1, col=1
)

# Add the annualized percentage difference time series to the panel below
for future in df['future'].unique():
    future_data = df[df['future'] == future]
    fig.add_trace(
        go.Scatter(x=future_data['timestamp'], y=future_data['annualized_percentage_diff'],
                   name=f"{future} Annualized Diff"),
        row=2, col=1
    )

# Update layout
fig.update_layout(height=1920, width=1080, title_text="Index Price and Annualized Percentage Difference Over Time")
fig.update_xaxes(title_text="Timestamp", row=2, col=1)
fig.update_yaxes(title_text="Index Price", row=1, col=1)
fig.update_yaxes(title_text="Annualized % Diff", row=2, col=1)

# Show plot
fig.show()
