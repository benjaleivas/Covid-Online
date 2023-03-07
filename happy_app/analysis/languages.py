import pandas as pd
from dash import dcc
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


def plot_languages():
    """
    Make a bubble chart of browser language for those with over 100M visits.

    Design based on Towards Data Science Waffle Chart:
        https://towardsdatascience.com/9-visualizations-to-show-proportions-or-percentages-instead-of-a-pie-chart-4e8d81617451

    Inputs: None.

    Returns (object): DCC Graph.
    """
    # Load data
    data = pd.read_csv(
        "happy_app/data/language.csv", usecols=["language_name", "visits"]
    )

    # Transform data
    data = data.groupby("language_name", as_index=False).sum()
    data["percentage"] = round((data.visits / data["visits"].sum()) * 100, ndigits=1)
    data = data.sort_values(by="visits", ascending=False)
    data = data[data.visits > 100000000]
    data["visits"] = round(data.visits / 1000000, ndigits=1)

    # Set features for figure
    languages = data.language_name.unique()
    palette = list(
        sns.color_palette(palette="Paired", n_colors=len(languages)).as_hex()
    )

    label = [
        i + "<br>" + str(j) + "M" + "<br>" + str(k) + "%"
        for i, j, k in zip(data.language_name, data.visits, data.percentage)
    ]

    data["Y"] = [1] * len(data)
    data["X"] = list(range(0, len(data)))

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
    fig.update_layout(
        width=900, height=320, margin=dict(t=50, l=0, r=0, b=0), showlegend=False
    )
    fig.update_traces(textposition="top center")
    fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_layout({"plot_bgcolor": "white", "paper_bgcolor": "white"})

    return dcc.Graph(id=f"languages", figure=fig)
