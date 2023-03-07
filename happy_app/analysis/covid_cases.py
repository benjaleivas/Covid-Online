import pandas as pd
from dash import dcc
import datetime as dt
from plotly_calplot import calplot
from happy_app.analysis.dashboard_math import get_covid_cases_data


def plot_covid_cases(year):
    """
    Creates Covid-19 calendar heatmap for chosen 'year'.
    
    Inputs: year (int): year to plot Covid-19 data for.

    Returns (object): DCC graph.
    """
    #Load data
    data = get_covid_cases_data(year)

    #Create figure
    fig = calplot(
        data,
        x='date',
        y='daily_cases',
        years_title=False,
        showscale=True,
        colorscale='blues'
    )

    return dcc.Graph(id=f'covid_daily_cases-{year}', figure=fig)
