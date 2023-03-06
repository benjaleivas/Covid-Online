import datetime
import numpy as np
import pandas as pd
from dash import dcc
import plotly.graph_objects as go
from datetime import datetime as dt
from happy_app.collect.utils import KEY_DATES

def plot_domain_visits(key_sites):
    """
    Plots domain's cumulative visits between 2019-2022.

    Input:
        - key_sites (list of str): list of domains to highlight in plot.

    Returns (object): DCC Graph.
    """
    #Specify parameters
    start_year = 2019
    number_weeks = 212
    y_range = 5500000000
    line_width = 3
    line_dict= {key_sites[0]:'solid'}
    color_dict = {key_sites[0]: '#1E90FF'}
    tick_weeks = [1,14,27,40,54,67,80,93,107,120,133,146,160,173,186,199]
    tick_texts = ['2019','Apr','Jul','Oct','2020','Apr','Jul','Oct','2021', 'Apr', 'Jul', 'Oct', '2022', 'Apr', 'Jul', 'Oct']
    
    if len(key_sites) == 5:
        start_year = 2020
        number_weeks = 159
        y_range = 160000000
        line_width = 2
        line_types = ['solid', 'dash', 'solid', 'dash', 'solid']
        line_colors = ['#9400D3', '#9400D3', '#7bccc4', '#7bccc4', '#0868ac']
        line_dict = dict()
        color_dict = dict()
        for i in range(len(key_sites)):
            line_dict[key_sites[i]] = line_types[i]
            color_dict[key_sites[i]] = line_colors[i]
        tick_weeks = [1,14,27,40,54,67,80,93,107,120,133,146]
        tick_texts = ['2020','Apr','Jul','Oct','2021','Apr','Jul','Oct','2022','Apr','Jul','Oct']

    #Load data
    data = pd.DataFrame(columns=['year', 'week', 'domain', 'visits'])
    for year in range(start_year,2022+1):
        all_sites = pd.read_csv(f'happy_app/data/update_data/{year}_all_sites.csv')
        data = pd.concat([data, all_sites], ignore_index=True)

    #Transform data
    idx = pd.MultiIndex.from_product(
        [data.year.unique(), data.week.unique(), data.domain.unique()], 
        names=['year', 'week', 'domain']
    )
    data = data.set_index(['year', 'week', 'domain']).reindex(idx, fill_value=0).reset_index()
    data = data.sort_values(by=['domain', 'year', 'week'], ignore_index=True)
    data['visits'] = data['visits'].astype(int)
    data['visits_cum'] = data.groupby(['domain'])['visits'].cumsum()
    data['week_count'] = data.index % number_weeks + 1
    data = data[data['domain'].isin(key_sites)]

    #Define layout
    layout = go.Layout(
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        title=None,
        title_font_family=None,
        title_font_color=None,
        font_family='Arial',
        font_color=None,
        font_size=14,
        showlegend=True,
        legend=dict(
            x=1,
            y=1.02,
            xanchor='right',
            yanchor='bottom',
            orientation='h'
        ),
        yaxis_title=None, 
        xaxis_title=None,
        xaxis=dict(
            tickmode = 'array',
            tickvals = tick_weeks,
            ticktext = tick_texts
            )
    )

    #Create figure
    fig = go.Figure()
    for site in key_sites:
        line_color = color_dict[site]
        subset = data[data['domain'] == site]
        fig.add_trace(
            go.Scatter(
                x = subset['week_count'],
                y = subset['visits_cum'],
                mode='lines',
                name=site,
                line=dict(
                    shape='linear',
                    width=line_width,
                    color=color_dict[site],
                    dash=line_dict[site]
                )
            )
        )

    #Add events
    events = dict()
    if len(key_sites) == 1:
        events['2020-03-13'] = KEY_DATES['2020-03-13']
    else:
        events['2020-12-11'] = 'FDA <br> Authorizes <br> Pfizer <br> Vaccine'
        events['2021-03-08'] = 'CDC Approves Safe Gathering <br> for Vaccinated Individuals'
        events['2022-01-19'] = 'Due to Omicron surge, <br> Biden launches online platform <br> to order free COVID-19 tests'
    
    for date, event in events.items():
        key_date = dt.strptime(date, '%Y-%m-%d')
        diff_year = key_date.year - start_year
        week = datetime.date(key_date.year, key_date.month, key_date.day).isocalendar()[1] + (53 * diff_year)
        fig.add_vline(
            x=week,
            line_width=1,
            line_dash="solid",
            line_color="red",
            annotation_text=event
        )

    #Update figure
    fig.update_layout(layout)
    fig.update_xaxes(showticklabels=True)
    fig.update_yaxes(
        gridcolor="#eee",
        griddash="solid",
        gridwidth=0.5,
        range=[0, y_range]
    )

    #Return dash object
    return dcc.Graph(id=f'domain_visits-{len(key_sites)}', figure=fig)