import pandas as pd
import datetime as dt
from plotly_calplot import calplot  # pip install plotly-calplot

def plot_covid_cases(year,metric):
    """
    Creates Covid-19 calendar heatmap for chosen 'year' and 'metric'.
    Inputs:
        - year (int): year to plot covid data for.
        - metric (str): indicator to use, 'daily_cases' or 'log_difference'.
    Returns (object): DCC graph of 'year' calendar map for covid's 'metric'.
    """
    #Load data
    # data = pd.read_csv(f'happy_app/data/{year}_daily_covid_data.csv')
    data = pd.read_csv(f'happy_app/data/cleaned_covid_data.csv')

    #Transform data
    data = data[['date',f'{metric}']]
    data['date'] =  pd.to_datetime(data['date'])
    data = data.drop(data[data['date'].dt.year != year].index)


    #Plot figure
    fig = calplot(data,
                  x='date',
                  y=f'{metric}',
                  years_title=False,
                  showscale=True,
                  colorscale='blues'
                 )

    return dcc.Graph(id=f'covid_cases-{year}-{metric}', figure=fig)
