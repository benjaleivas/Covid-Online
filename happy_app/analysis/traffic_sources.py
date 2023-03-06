import pandas as pd
from dash import dcc
import plotly.graph_objects as go

def plot_traffic_sources():
    """
    Plots horizontal stacked bar chart with visits from categorized traffic
    sources (Search Engines, Direct Links, Government Sites, Social Media, and
    Other), by COVID peak (March 2020 - April 2020, Dec 2020 - Jan 2021, 
    Dec 2021 - Jan 2022).

    Returns (object): DCC Graph.
    """

    #Load data
    mar_2020_apr_2020 = pd.read_csv('happy_app/data/update_data/2020-03-01_to_2020-04-30_traffic-source.csv', usecols=['source type', 'visits'])
    dec_2020_jan_2021 = pd.read_csv('happy_app/data/update_data/2020-12-01_to_2021-01-31_traffic-source.csv', usecols=['source type', 'visits'])
    dec_2021_jan_2022 = pd.read_csv('happy_app/data/update_data/2021-12-01_to_2022-01-31_traffic-source.csv', usecols=['source type', 'visits'])
    datasets = [dec_2021_jan_2022, dec_2020_jan_2021, mar_2020_apr_2020]

    #Transform data
    search_engine_visits = []
    direct_link_visits = []
    gov_sites_visits = []
    social_media_visits = []
    other_sources_visits = []

    for data in datasets:
        data = data.groupby('source type', as_index=False).sum()
        search_engine_visits.append(data.loc[data['source type']=='Search Engine', 'visits'].values[0])
        direct_link_visits.append(data.loc[data['source type']=='Direct Link', 'visits'].values[0])
        gov_sites_visits.append(data.loc[data['source type']=='.gov Sites', 'visits'].values[0])
        social_media_visits.append(data.loc[data['source type']=='Social Media', 'visits'].values[0])
        other_sources_visits.append(data.loc[data['source type']=='Other', 'visits'].values[0])

    source_visits = [
        search_engine_visits, 
        direct_link_visits, 
        gov_sites_visits, 
        social_media_visits, 
        other_sources_visits]

    #Define layout
    layout = go.Layout(
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        font_family='Arial',
        font_size=20,
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

    #Define y-categories, bar colors and legend labels
    colors = ['#104E8B', '#1E90FF', '#008000', '#FFFF00', '#C1CDCD']
    peaks = ['Dec 2021 - Jan 2022', 'Dec 2020 - Jan 2021', 'Mar 2020 - Apr 2020']
    sources = ['Search Engine','Direct Link','.gov Sites','Social Media','Other']

    #Create figure
    fig = go.Figure()
    for i in range(len(sources)):
        fig.add_trace(
            go.Bar(
                y=peaks,
                x=source_visits[i],
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

    #Return dash object
    return dcc.Graph(id=f'traffic_sources', figure=fig)
