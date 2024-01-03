# Importing necessary libraries
import pandas as pd
from sqlalchemy import create_engine
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Database connection details
db_params = "postgresql://postgres:example@127.0.0.1:5432/mydb"
engine = create_engine(db_params)

# SQL Query to fetch data for 'BTC-5JAN24' contract
query = """
SELECT timestamp, entry_carry, exit_carry, market_delta_fut
FROM futures_data
WHERE future = 'BTC-5JAN24'
"""

# Reading data from the database into a DataFrame
df = pd.read_sql(query, engine)

# Creating a Plotly figure with subplots
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1,
                    subplot_titles=('Carry Enter & Exit', 'Market Delta Future'),
                    row_heights=[0.7, 0.3])

# Adding entry_carry and exit_carry to the main plot
fig.add_trace(go.Scatter(x=df['timestamp'], y=df['entry_carry'], mode='lines', name='entry_carry'), row=1, col=1)
fig.add_trace(go.Scatter(x=df['timestamp'], y=df['exit_carry'], mode='lines', name='exit_carry'), row=1, col=1)

# Adding market_delta_fut to the subplot
fig.add_trace(go.Scatter(x=df['timestamp'], y=df['market_delta_fut'], mode='lines', name='market_delta_fut'), row=2, col=1)

# Update xaxis properties
fig.update_xaxes(
    type="date",  # Ensuring the type is date
    tickformat="%H:%M:%S",  # Formatting to show hours, minutes, and seconds
    tickangle=-45,  # Angle of the text for better readability
    tickwidth=2, 
    tickcolor='blue',
    nticks=20,  # Adjust the number of ticks for clarity
)

# Updating layout for a better widescreen fit
fig.update_layout(height=1080, width=1920, title_text="BTC-5JAN24 Analysis")

# Save the plot to HTML file
#fig.write_html("BTC-5JAN24_analysis.html")
fig.show()