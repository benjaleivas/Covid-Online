import pandas as pd
from dash import dcc
import plotly.graph_objects as go

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

#Plot graph
fig = go.Figure()
fig.add_trace(
    go.Bar(
        y=['Dec 2021 - Jan 2022','Dec 2020 - Jan 2021','Mar 2020 - Apr 2020'],
        x=search_engine_visits,
        name='Search Engine',
        orientation='h',
        marker=dict(
            color='#104E8B',
            line=dict(
                color='#104E8B',
                width=1
            )
        )
    )
)

fig.add_trace(
    go.Bar(
        y=['Dec 2021 - Jan 2022','Dec 2020 - Jan 2021','Mar 2020 - Apr 2020'],
        x=direct_link_visits,
        name='Direct Link',
        orientation='h',
        marker=dict(
            color='#1E90FF',
            line=dict(
                color='#1E90FF',
                width=1
            )
        )
    )
)

fig.add_trace(
    go.Bar(
        y=['Dec 2021 - Jan 2022','Dec 2020 - Jan 2021','Mar 2020 - Apr 2020'],
        x=gov_sites_visits,
        name='.gov Sites',
        orientation='h',
        marker=dict(
            color='green',
            line=dict(
                color='green',
                width=1
            )
        )
    )
)

fig.add_trace(
    go.Bar(
        y=['Dec 2021 - Jan 2022','Dec 2020 - Jan 2021','Mar 2020 - Apr 2020'],
        x=social_media_visits,
        name='Social Media',
        orientation='h',
        marker=dict(
            color='yellow',
            line=dict(
                color='yellow',
                width=1
            )
        )
    )
)

fig.add_trace(
    go.Bar(
        y=['Dec 2021 - Jan 2022','Dec 2020 - Jan 2021','Mar 2020 - Apr 2020'],
        x=other_sources_visits,
        name='Other',
        orientation='h',
        marker=dict(
            color='#C1CDCD',
            line=dict(
                color='#C1CDCD',
                width=1
            )
        )
    )
)

fig.update_layout(layout)
fig.show()
