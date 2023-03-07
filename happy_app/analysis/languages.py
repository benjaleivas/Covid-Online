import pandas as pd
from dash import dcc
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
from happy_app.analysis.dashboard_math import get_languages_data


def plot_languages():
    """
    Make a bubble chart of browser language for those with over 100M visits.

    Design based on Towards Data Science Bubble Chart:
        https://towardsdatascience.com/9-visualizations-to-show-proportions-or-percentages-instead-of-a-pie-chart-4e8d81617451

    Inputs: None.

    Returns (object): DCC Graph.
    """
    # Load data
    data = get_languages_data()

    # Set features
    languages = data.language_name.unique()
    palette = list(
        sns.color_palette(
            palette="Paired", 
            n_colors=len(languages)
        ).as_hex()
    )
    label = [
        i + "<br>" + str(j) + "M" + "<br>" + str(k) + "%"
        for i, j, k in zip(data.language_name, data.visits, data.percentage)
    ]

    #Create figure
    fig = px.scatter(
        data,
        x=data["X"],
        y=data["Y"],
        color="language_name",
        color_discrete_sequence=palette,
        size="visits",
        text=label,
        size_max=90,
    )

    #Update figure
    fig.update_layout(
        width=900, 
        height=320, 
        showlegend=False,
        margin=dict(t=50, l=0, r=0, b=0) 
    )
    fig.update_traces(textposition="top center")
    fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_layout({"plot_bgcolor": "white", "paper_bgcolor": "white"})

    return dcc.Graph(id=f"languages", figure=fig)
