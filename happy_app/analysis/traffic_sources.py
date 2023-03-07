import pandas as pd
from dash import dcc
import plotly.graph_objects as go
from happy_app.analysis.dashboard_math import get_traffic_sources_data


def plot_traffic_sources():
    """
    Plots horizontal stacked bar chart with visits from categorized traffic
    sources (Search Engines, Direct Links, Government Sites, Social Media, and
    Other), by COVID peak (March 2020 - April 2020, Dec 2020 - Jan 2021, 
    Dec 2021 - Jan 2022).

    Inputs: None.

    Returns (object): DCC Graph.
    """
    #Load data
    data = get_traffic_sources_data()

    #Define layout
    layout = go.Layout(
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        font_family='Arial',
        font_size=12,
        showlegend=True,
        barmode='stack',
        legend=dict(
            x=1,
            y=1.02,
            xanchor='right',
            yanchor='bottom',
            orientation='h',
            traceorder='normal'
        )
    )

    #Set bar colors, y-axis categories, and legend labels
    colors = ['#104E8B', '#1E90FF', '#008000', '#FFFF00', '#C1CDCD']
    peaks = ['Dec 2021 - Jan 2022', 'Dec 2020 - Jan 2021', 'Mar 2020 - Apr 2020']
    sources = ['Search Engine','Direct Link','.gov Sites','Social Media','Other']

    #Create figure
    fig = go.Figure()
    for i in range(len(sources)):
        fig.add_trace(
            go.Bar(
                y=peaks,
                x=data[i],
                name=sources[i],
                orientation='h',
                marker=dict(
                    color=colors[i],
                    line=dict(
                        color=colors[i],
                        width=1
                    )
                )
            )
        )    

    #Update layout
    fig.update_layout(layout)

    return dcc.Graph(id=f'traffic_sources', figure=fig)
