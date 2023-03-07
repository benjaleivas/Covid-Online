import datetime
import numpy as np
import pandas as pd
from dash import dcc
import plotly.graph_objects as go
from datetime import datetime as dt
from happy_app.collect.utils import KEY_DATES
from happy_app.analysis.dashboard_math import get_cdc_visits_data


def plot_cdc_visits():
    """
    Plots CDCs website cumulative visits between 2019-2022.

    Inputs: None.

    Returns (object): DCC Graph.
    """
    #Load data
    data = get_cdc_visits_data()

    #Define layout
    layout = go.Layout(
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        font_family='Arial',
        font_size=14,
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
                        54, 67, 80, 93,\
                        107, 120, 133, 146,\
                        160, 173, 186, 199],
            ticktext = ['2019', 'Apr', 'Jul', 'Oct', \
                        '2020', 'Apr', 'Jul', 'Oct', \
                        '2021', 'Apr', 'Jul', 'Oct', \
                        '2022', 'Apr', 'Jul', 'Oct']
            )
    )

    #Create figure
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x = data['week_count'],
            y = data['visits_cum'],
            mode='lines',
            name='cdc.gov',
            line=dict(
                shape='linear',
                width=3,
                color='#1E90FF',
                dash='solid'
            )
        )
    )

    #Add relevant events    
    for date, event in KEY_DATES.items():
        key_date = dt.strptime(date, '%Y-%m-%d')
        diff_year = key_date.year - 2019
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
        break

    #Update figure
    fig.update_layout(layout)
    fig.update_xaxes(showticklabels=True)
    fig.update_yaxes(
        gridcolor="#eee",
        griddash="solid",
        gridwidth=0.5,
        range=[0, 5500000000]
    )

    return dcc.Graph(id=f'cdc_visits', figure=fig)
