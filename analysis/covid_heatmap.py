import numpy as np
import pandas as pd
from plotly_calplot import calplot  # pip install plotly-calplot

#Load merged data
data = pd.read_csv('data/merged_test_dataset.csv',  usecols=['date', 
                                                             'visits', 
                                                             'cases', 
                                                             'daily_cases', 
                                                             'deaths', 
                                                             'daily_deaths'])

#Transform data
data['date'] = pd.to_datetime(data['date'])
#data = data[data['date'].dt.year == 2022]                      #filter year
#data['daily_cases_diff'] = data.daily_cases.diff().fillna(0)   #differences
#data = data[['date', 'daily_cases']]                           #relevant vars

#Plot heatmap
fig = calplot(
         data,
         x="date",
         y="daily_cases",
         years_title=False,
         showscale=True,
         colorscale='reds'
)

fig.show()

app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

app.run_server(debug=True, use_reloader=False)

graph = dcc.Graph(id='visits_trend', figure=fig)
dcc.Download(id='visits_trend')

