import pandas as pd
import datetime as dt
from plotly_calplot import calplot  # pip install plotly-calplot

#Covid data
covid_2020 = pd.read_csv('data/2020_daily_covid_data.csv')
covid_2021 = pd.read_csv('data/2021_daily_covid_data.csv')
covid_2022 = pd.read_csv('data/2022_daily_covid_data.csv')

def covid_map(year,metric):
    """
    DESCRIPTION
    INPUTS
    RETURN
    """
    #Load data
    data = pd.read_csv(f'data/cleaned_covid_data.csv')

    #Transform data
    data = data[['date',f'{metric}']]
    data['date'] =  pd.to_datetime(data['date'])
    data = data.drop(data[pd.to_datetime(data['date']).dt.year != year].index)

    #Plot figure
    fig = calplot(data,
                  x='date',
                  y=f'{metric}',
                  years_title=False,
                  showscale=True,
                  colorscale='blues'
                 )

    return dcc.Graph(id='covid', figure=fig)

# #Load merged data
# data = pd.read_csv('data/merged_test_dataset.csv',  usecols=['date', 
#                                                              'visits', 
#                                                              'cases', 
#                                                              'daily_cases', 
#                                                              'deaths', 
#                                                              'daily_deaths'])

# #Transform data
# data['date'] = pd.to_datetime(data['date'])
# #data = data[data['date'].dt.year == 2022]                      #filter year
# #data['daily_cases_diff'] = data.daily_cases.diff().fillna(0)   #differences
# #data = data[['date', 'daily_cases']]                           #relevant vars

# #Plot heatmap
# fig = calplot(
#          data,
#          x="date",
#          y="daily_cases",
#          years_title=False,
#          showscale=True,
#          colorscale='blues'
# )

# fig.show()

# app = dash.Dash()
# app.layout = html.Div([
#     dcc.Graph(figure=fig)
# ])

# app.run_server(debug=True, use_reloader=False)

# graph = dcc.Graph(id='visits_trend', figure=fig)
# dcc.Download(id='visits_trend')

