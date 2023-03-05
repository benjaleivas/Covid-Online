import datetime
import numpy as np
import pandas as pd
from dash import dcc
import plotly.graph_objects as go
from datetime import datetime as dt
from happy_app.collect.utils import KEY_DATES

def plot_domain_visits(key_sites):
    """
    Plots specific domain visits for year, and its relative percentage with
    respect to HHS visits.

    Input:
        - key_domains (list): list of domains to highlight in plot.
    
    Returns (object): DCC Graph.
    """
    #Prepare data
    data = pd.DataFrame(columns=['year', 'week', 'domain', 'visits'])
    for year in range(2019,2022+1):
        all_sites = pd.read_csv(f'happy_app/data/update_data/{year}_all_sites.csv')
        data = pd.concat([data, all_sites], ignore_index=True)

    #Transform data
    idx = pd.MultiIndex.from_product([data.year.unique(), data.week.unique(), data.domain.unique()], names=['year', 'week', 'domain'])
    data = data.set_index(['year', 'week', 'domain']).reindex(idx, fill_value=0).reset_index()
    data = data.sort_values(by=['domain', 'year', 'week'], ignore_index=True)
    data['visits'] = data['visits'].astype(int)
    data['visits_cum'] = data.groupby(['domain'])['visits'].cumsum()
    data['week_count'] = data.index % 53 + 1
    data = data.sort_values(by=['domain', 'year', 'week'], ignore_index=True)

    #Define layout
    layout = go.Layout(paper_bgcolor='rgba(0,0,0,0)', 
                       plot_bgcolor='rgba(0,0,0,0)',
                       title=None,
                       title_font_family=None,
                       title_font_color=None,
                       font_family='Arial',
                       font_color=None,
                       yaxis_title=None, 
                       xaxis_title=None)

    #Define lines formats
    line_color_all_sites = ['#C1CDCD']
    line_colors_key_sites = ['red', 'blue', 'green', 'yellow', 'purple', 'black']
    line_names = key_sites

    #Create figure
    fig = go.Figure()
    for domain in data.domain.unique():
        fig.add_trace(go.Scatter(x = datasets[idx]['week'],
                                 y = datasets[idx]['visits'],
                                 mode='lines',
                                 name=line_names[idx],
                                 line=dict(shape='linear', 
                                           color=line_colors[idx], 
                                           dash=line_types[idx])))