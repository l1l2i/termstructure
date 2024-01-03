import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as plt_io


daydf = pd.read_csv('spy_day.csv', parse_dates=['date'])
mindf = pd.read_csv('spy_minute.csv', parse_dates=['date'])

colors = px.colors.qualitative.Plotly

def style_and_save_chart(fig: go.Figure, title: str) -> go.Figure:
    fig.update_traces(line=dict(color=colors[4], width=1), marker=dict(color=colors[4]))
    fig.update_xaxes(showline=True, linewidth=1, linecolor='gray', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='gray', mirror=True)
    fig.update_layout(
        font_color="gray",
        title=title,
        title_font_color="white",
        template='plotly_dark',
        xaxis_title="Date",
        yaxis_title="Price",
    )
    fig.write_image(title.replace(' ', '_').lower() + ".png", scale=2)
    return fig

df = daydf
fig = go.Figure()
fig.add_trace(go.Scatter(x=df.date, y=df.close, mode='lines'))
style_and_save_chart(fig, title='Daily Price Data')

df = daydf[(daydf.date >= '2021-05-24') & (daydf.date <= '2021-06-19')]
fig = go.Figure()
fig.add_trace(go.Scatter(x=df.date, y=df.close, mode='lines'))
fig.update_layout(xaxis_tick0 = df['date'].iloc[0], xaxis_dtick=86400000)
style_and_save_chart(fig, title='Daily Price Data - Zoomed In')

df = daydf[(daydf.date >= '2021-05-24') & (daydf.date <= '2021-06-19')]
fig = go.Figure()
fig.add_trace(go.Scatter(x=df.date, y=df.close, mode='markers'))
fig.update_layout(xaxis_tick0 = df['date'].iloc[0], xaxis_dtick=86400000)
style_and_save_chart(fig, title='Daily Price Data - Points Showing Gaps')

df = daydf[(daydf.date >= '2021-05-24') & (daydf.date <= '2021-06-19')]
fig = go.Figure()
fig.add_trace(go.Scatter(x=df.date, y=df.close, mode='markers'))
fig.update_xaxes(
    rangebreaks=[
        dict(bounds=["sat", "mon"]),
        dict(values=["2021-05-31"]) # Memorial Day
    ]
)
fig.update_layout(xaxis_tick0 = df['date'].iloc[0], xaxis_dtick=86400000)
style_and_save_chart(fig, title='Daily Price Data - Points No Gaps')

df = mindf
fig = go.Figure()
fig.add_trace(go.Scatter(x=df.date, y=df.close))
style_and_save_chart(fig, title='Minute Price Data')

df = mindf
fig = go.Figure()
fig.add_trace(go.Scatter(x=df.date, y=df.close, mode="markers", marker=dict(size=1)))
style_and_save_chart(fig, title='Minute Price Data - Points')

df = mindf
fig = go.Figure()
fig.add_trace(go.Scatter(x=df.date, y=df.close))
fig.update_xaxes(
    rangebreaks=[
        dict(bounds=[16, 9.5], pattern="hour")
    ]
)
style_and_save_chart(fig, title='Minute Price Data - No Overnight Time Gaps')

df = mindf
fig = go.Figure()
fig.add_trace(go.Scatter(x=df.date, y=df.close))
fig.update_xaxes(
    rangebreaks=[
        dict(bounds=["sat", "mon"]),
        dict(bounds=[16, 9.5], pattern="hour")
    ]
)
style_and_save_chart(fig, title='Minute Price Data - No Overnight or Weekend Gaps')

