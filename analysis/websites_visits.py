import numpy as np
import pandas as pd
from dash import dcc
from scipy import stats
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#Load merged data
data = pd.read_csv('data/merged_test_dataset.csv', usecols=['date', 'visits', 'cases', 'daily_cases', 'deaths', 'daily_deaths'])

#Transform data
data['date'] = pd.to_datetime(data['date'])
data['visits_2019'] = data.visits/1.5
#data = data[data['date'].dt.year == 2022]                      #filter year
#data['daily_cases_diff'] = data.daily_cases.diff().fillna(0)   #differences
#data = data[['date', 'daily_cases']]                           #relevant vars
# data['visits_norm'] = stats.zscore(data['visits']) # NORMALIZE TO SAME YEAR OR 2019?

#Layout
layout = go.Layout(paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(0,0,0,0)',
                title="Daily visits to government websites (in millions)",
                title_font_family='Times New Roman',
                title_font_color=None,
                font_family='Arial',
                font_color=None,
                yaxis_title=None, 
                xaxis_title=None)
                # xaxis = go.layout.XAxis(showticklabels=False),
                # yaxis = go.layout.YAxis(title=None))

# trace_2021 = go.Scatter(
#     x = data['date'], 
#     y = data['visits'], 
#     mode='lines',
#     name="2021",
#     line=dict(shape='linear', color='#1C86EE', dash='solid')
# )

# trace_2019 = go.Scatter(
#     x = data['date'], 
#     y = data['visits_2019'], 
#     mode='lines',
#     name="2019",
#     line=dict(shape='linear', color="#C1CDCD", dash='dash')
# )

# trace_diff = go.Scatter(
#     x = data['date'], 
#     y = data['visits']-data["visits_2019"], 
#     mode='lines',
#     name="Difference",
#     line=dict(shape='linear', color='red', dash='solid')
# )

# layout = dict(
#     paper_bgcolor='rgba(0,0,0,0)', 
#     plot_bgcolor='rgba(0,0,0,0)',
#     title="Daily visits to government websites (in millions)",
#     title_font_family='Times New Roman',
#     title_font_color=None,
#     font_family='Arial',
#     font_color=None,
#     yaxis_title=None, 
#     xaxis_title=None
# )

# data = [trace_2021, trace_2019, trace_diff]
# fig = go.Figure(data=data, layout=layout)
# fig.show()

#Create visualization
fig = make_subplots(rows=2, 
                    cols=1,
                    x_title=None,
                    y_title=None,
                    # shared_xaxes=True,
                    subplot_titles=None)

#Government website visits (transform visits to weekly to avoid weekend drops)
#2021
fig.add_trace(go.Scatter(x = data['date'], 
                         y = data['visits'], 
                         mode='lines',
                         name="2021",
                         line=dict(shape='linear', color='#1C86EE', dash='solid')),
              row=1, col=1)
#2019
fig.add_trace(go.Scatter(x = data['date'], 
                         y = data['visits_2019'], 
                         mode='lines',
                         name="2019",
                         line=dict(shape='linear', color="#C1CDCD", dash='dash')), 
              row=1, col=1)
#Difference
fig.add_trace(go.Scatter(x = data['date'], 
                         y = data['visits']-data["visits_2019"], 
                         mode='lines',
                         name="Difference",
                         line=dict(shape='linear', color='red', dash='solid')),
              row=1, col=1)

fig.update_layout(layout)
fig.update_xaxes(showticklabels=False)
fig.update_yaxes(gridcolor="#eee", griddash="solid", gridwidth=0.5, 
                range=[0, max(max(data['visits']), max(data['visits_2019']))+3000000])

fig.show()

graph = dcc.Graph(id='visits_trend', figure=fig)
