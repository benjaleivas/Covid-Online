import pandas as pd
from dash import dcc
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_visits_vs_2019(year):
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

    #Create figure
    fig = make_subplots(rows=1,
                        cols=1,
                        x_title=None,
                        y_title=None,
                        subplot_titles=None)

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

    #Add traces
    line_types = ['solid', 'solid', 'dash']
    line_colors = ['#1E90FF', '#C1CDCD', '#CD2626']
    line_names = [f'{year}', 'Baseline (2019)', 'Difference with baseline']

    for idx in range(len(datasets)):
        fig.add_trace(go.Scatter(x = datasets[idx]['week'],
                                 y = datasets[idx]['visits'],
                                 mode='lines',
                                 name=line_names[idx],
                                 line=dict(shape='linear', 
                                           color=line_colors[idx], 
                                           dash=line_types[idx])))

    #Add events (Create dictionary for this in 'data' folder)
    # event_2020_1 = {'year': 2021, 'month': 3, 'day': 13, 'event': 'Event 1'} 
    # event_2020_2 = {'year': 2021, 'month': 7, 'day': 2, 'event': 'Event 2'} 
    # event_2020_3 = {'year': 2021, 'month': 11, 'day': 29, 'event': 'Event 3'} 
    # events_2020 = [event_1, event_2, event_3]

    # for event in events:
    #     fig.add_vline(x=datetime.datetime(
    #                     event['year'],event['month'],event['day']).timestamp()*1000, 
    #                     line_width=1, 
    #                     line_dash="solid", 
    #                     line_color="red", 
    #                     annotation_text=event['event'])

    #Update figure
    fig.update_layout(layout)
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(gridcolor="#eee",
                     griddash="solid",
                     gridwidth=0.5,
                     range=[0, 250000000])

    #Return dash object
    # return fig.show()
    return dcc.Graph(id='visits', figure=fig)
