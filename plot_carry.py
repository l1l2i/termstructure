# Importing necessary libraries
import pandas as pd
from sqlalchemy import create_engine
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Database connection details


db_params = "postgresql://postgres:example@127.0.0.1:5432/mydb"

engine = create_engine(db_params)

# Establishing a connection to the database
#engine = create_engine(f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}')

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

# Adding carry_inter and carry_exit to the main plot
fig.add_trace(go.Scatter(x=df['timestamp'], y=df['entry_carry'], mode='lines', name='entry_carry'), row=1, col=1)
fig.add_trace(go.Scatter(x=df['timestamp'], y=df['exit_carry'], mode='lines', name='exit_carry'), row=1, col=1)

# Adding market_delta_fut to the subplot
fig.add_trace(go.Scatter(x=df['timestamp'], y=df['market_delta_fut'], mode='lines', name='market_delta_fut'), row=2, col=1)

# Updating layout for a better widescreen fit
fig.update_layout(height=1080, width=1920, title_text="BTC-5JAN24 Analysis")

# Displaying the plot
fig.show()
#fig.write_html("BTC-5JAN24_analysis.html")





#import plotly.graph_objects as go
#import plotly.express as px

#df1 = px.data.gapminder().query("country in ['Canada']")
#df2 = px.data.gapminder().query("country in ['Italy']")

#fig = go.Figure()
#fig.add_trace(go.Scatter(x=df["timestamp"], y=df["entry_carry"], mode='lines', name='entry_carry'))
#fig.add_trace(go.Scatter(x=df["timestamp"], y=df["exit_carry"], mode='lines', name='exit_carry'))
#fig.show()