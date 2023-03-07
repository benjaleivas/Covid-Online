import pandas as pd
from dash import dcc
import datetime as dt
from plotly_calplot import calplot

def plot_covid_cases(year):
    """
    Creates Covid-19 calendar heatmap for chosen 'year'.
    
    Inputs: year (int): year to plot Covid-19 data for.

    Returns (object): DCC graph.
    """
    #Load data
    data = pd.read_csv(f'happy_app/data/{year}_daily_covid_data.csv')

    #Transform data
    data = data[['date','daily_cases']]
    data['date'] =  pd.to_datetime(data['date'])

    #Create figure
    fig = calplot(
        data,
        x='date',
        y='daily_cases',
        years_title=False,
        showscale=True,
        colorscale='blues'
    )

    #Return dash object
    return dcc.Graph(id=f'covid_daily_cases-{year}', figure=fig)
