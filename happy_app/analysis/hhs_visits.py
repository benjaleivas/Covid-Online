import datetime
import pandas as pd
from dash import dcc
import plotly.graph_objects as go
from datetime import datetime as dt
from happy_app.collect.utils import KEY_DATES

def plot_hhs_visits(year):
    """
    Plots trend of visits to HHS's website for 'year' relative to 2019, as well
    as the difference in visits between both years.

    Inputs:
        - year (int): year to compare 2019's visits to.

    Returns (object): DCC Graph.
    """
    #Load data
    post, prev = [pd.read_csv(f'happy_app/data/update_data/{year}_total_hhsvisits_by_week.csv'),
                 pd.read_csv('happy_app/data/update_data/2019_total_hhsvisits_by_week.csv')]
    diff = post[['week']]
    diff['visits'] = post.visits - prev.visits
    datasets = [post, prev, diff]

    #Define layout
    layout = go.Layout(
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        font_family='Arial',
        showlegend=True,
        legend=dict(
            x=1,
            y=1.02,
            xanchor='right',
            yanchor='bottom',
            orientation='h'
        )
    )

    #Define lines formats
    line_types = ['solid', 'solid', 'dash']
    line_colors = ['#1E90FF', '#C1CDCD', '#CD2626']
    line_names = [f'{year}', 'Baseline (2019)', 'Difference with baseline']

    #Create figure
    fig = go.Figure()
    for idx in range(len(datasets)):
        fig.add_trace(
            go.Scatter(
                x = datasets[idx]['week'],
                y = datasets[idx]['visits'],
                mode='lines',
                name=line_names[idx],
                line=dict(
                    shape='linear', 
                    color=line_colors[idx], 
                    dash=line_types[idx]
                )
            )
        )

    #Add events
    for date, event in KEY_DATES.items():
        key_date = dt.strptime(date, '%Y-%m-%d')
        if year == key_date.year:
            week = datetime.date(key_date.year, key_date.month, key_date.day).isocalendar()[1]
            fig.add_vline(
                x=week,
                line_width=1, 
                line_dash="solid", 
                line_color="red", 
                annotation_text=event
            )

    #Update figure
    fig.update_layout(layout)
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(
        gridcolor="#eee",
        griddash="solid",
        gridwidth=0.5,
        range=[0, 250000000]
    )

    #Return dash object
    return dcc.Graph(id=f'hhs_visits-{year}', figure=fig)
