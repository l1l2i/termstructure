import plotly.express as px
import pandas as pd





# pandas data frame
df = pd.DataFrame({'x': [1, 2, 3, 4, 5, 6, 7],
                  'y': [10, 15, 25, 18, 43, 30, 65]})

fig = px.line(df, x = 'x', y = 'y', markers = True)
fig.update_traces(line = dict(dash = "dot", width = 4, color = "red"),
                  marker = dict(color = "darkblue", size = 20, opacity = 0.8))

fig.show() 
 


fig = px.line(df, x = df['timestamp'], y = df['entry_carry'], markers = True)
fig.update_traces(line = dict(dash = "dot", width = 4, color = "red"),
                  marker = dict(color = "darkblue", size = 20, opacity = 0.8))

fig.show() 
 