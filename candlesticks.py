import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

djia = yf.Ticker("DJIA")
df = djia.history(start="2022-01-01", end="2022-12-31", interval="1d")
# color column add
df['colors'] = df[['Open', 'Close']].apply(lambda x: 'green' if x['Open'] <= x['Close'] else 'red', axis=1)

fig = go.Figure()
fig = make_subplots(rows=1, cols=1)

# candlestick
fig.append_trace(
    go.Candlestick(
        x=df.index,
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"]
    ), row=1, col=1
)
fig.add_trace(go.Scatter(mode='markers', x=df.index, y=[18]*len(df), marker=dict(size=5, color=df['colors'])),row=1, col=1)

fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])])
fig.update_layout(height=500)
fig.show()