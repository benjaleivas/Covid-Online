import datetime
import pandas as pd
from dash import dcc
import plotly.graph_objects as go
from datetime import datetime as dt
from happy_app.collect.utils import KEY_DATES
from happy_app.analysis.dashboard_math import get_domain_visits_data


def plot_domain_visits():
    """
    Plots key site's cumulative visits between 2020-2022.

    Inputs: None.

    Returns (object): DCC Graph.
    """
    #Load data
    data, key_sites = get_domain_visits_data()

    #Define layout
    layout = go.Layout(
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        font_family='Arial',
        font_size=10,
        showlegend=True,
        legend=dict(
            x=1,
            y=1.02,
            xanchor='right',
            yanchor='bottom',
            orientation='h'
        ),
        xaxis=dict(
            tickmode = 'array',
            tickvals = [1, 14, 27, 40, \
                        54, 67, 80, 93, \
                        107, 120, 133, 146],
            ticktext = ['2020', 'Apr', 'Jul', 'Oct', \
                        '2021', 'Apr', 'Jul', 'Oct', \
                        '2022', 'Apr', 'Jul', 'Oct']
            )
    )

    #Define line format
    line_types = ['solid', 'dash', 'solid', 'dash', 'solid']
    line_colors = ['#9400D3', '#9400D3', '#7bccc4', '#7bccc4', '#0868ac']
    line_dict = dict()
    color_dict = dict()
    for i in range(len(key_sites)):
        line_dict[key_sites[i]] = line_types[i]
        color_dict[key_sites[i]] = line_colors[i]

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
                    width=2,
                    color=color_dict[site],
                    dash=line_dict[site]
                )
            )
        )

    #Add events
    relevant_dates = {'2020-12-11', '2021-03-08', '2022-01-19'}    
    for date, event in KEY_DATES.items():
        if date in relevant_dates:
            key_date = dt.strptime(date, '%Y-%m-%d')
            diff_year = key_date.year - 2020
            week = datetime.date(
                key_date.year, 
                key_date.month, 
                key_date.day
                ).isocalendar()[1] + (53 * diff_year)
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
        range=[0, 160000000]
    )

    return dcc.Graph(id='domain_visits', figure=fig)
