import pandas as pd
from dash import dcc
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def visits_vs_2019(year):
    """
    Plots trend of HHS's website visits.
    Input (int): year to compare to 2019.
    Returns (object): Graph of visits trends for 'year', 2019, and difference.
    """
    #Load data
    post, pre = [pd.read_csv(f'data/{year}_hhs_totalvisits_by_week.csv'),
                 pd.read_csv('data/2019_hhs_totalvisits_by_week.csv')]
    diff = post[['week']]
    diff['visits'] = post.visits - pre.visits
    datasets = [post, pre, diff]

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
                    #  range=[0, max(max(post.visits), max(pre.visits))])

    #Return dash object
    # return fig.show()
    return dcc.Graph(id='visits', figure=fig)

    # return fig.show()
    # app = dash.Dash()
    # app.layout = html.Div([
    #     dcc.Graph(figure=fig)
    # ])
    # app.run_server(debug=True, use_reloader=False)

####################################################################################################
# PREVIOUS CODE, DON'T ERASE YET
####################################################################################################

# #     #Baseline
# #     fig.add_trace(go.Scatter(x = visits_2019['week'],
# #                              y = visits_2019['visits'],
# #                              mode='lines',
# #                              name='2019',
# #                              line=dict(shape='linear', color='#1E90FF', dash='solid')))

# #     #Selected year
# #     fig.add_trace(go.Scatter(x = visits_2019['week'],
# #                              y = visits_2019['visits'],
# #                              mode='lines',
# #                              name='2019',
# #                              line=dict(shape='linear', color='#1E90FF', dash='solid')))


# # #2021
# # fig.add_trace(go.Scatter(x = visits_2021['week'],
# #                          y = visits_2021['visits'],
# #                          mode='lines',
# #                          name="2021",
# #                          line=dict(shape='linear', color='#1E90FF', dash='solid'))) #,
# # #2019
# # fig.add_trace(go.Scatter(x = visits_2019['week'],
# #                          y = visits_2019['visits'],
# #                          mode='lines',
# #                          name="Baseline (2019)",
# #                          line=dict(shape='linear', color="#C1CDCD", dash='dash'))) 
# # #Difference
# # fig.add_trace(go.Scatter(x = visits_2019['week'], 
# #                          y = visits_2021['visits']-visits_2019['visits'], 
# #                          mode='lines',
# #                          name="Difference",
# #                          line=dict(shape='linear', color='#CD2626', dash='solid')))

# fig.update_layout(layout)
# fig.update_xaxes(showticklabels=False)
# fig.update_yaxes(gridcolor="#eee", 
#                  griddash="solid", 
#                  gridwidth=0.5, 
#                 #  range=[0, 150000000])
#                  range=[0, max(max(visits_2021['visits']), max(visits_2019['visits']))])

# fig.show()


# #Add events
# event_1 = {'year': 2021, 'month': 3, 'day': 13, 'event': 'Event 1'} 
# event_2 = {'year': 2021, 'month': 7, 'day': 2, 'event': 'Event 2'} 
# event_3 = {'year': 2021, 'month': 11, 'day': 29, 'event': 'Event 3'} 
# events = [event_1, event_2, event_3]

# for event in events:
#     fig.add_vline(x=datetime.datetime(
#                     event['year'],event['month'],event['day']).timestamp()*1000, 
#                     line_width=1, 
#                     line_dash="solid", 
#                     line_color="red", 
#                     annotation_text=event['event'])

# fig.show()

# app = dash.Dash()
# app.layout = html.Div([
#     dcc.Graph(figure=fig)
# ])

# app.run_server(debug=True, use_reloader=False)

# graph = dcc.Graph(id='visits_trend', figure=fig)
# dcc.Download(id='visits_trend')


# # #Load merged data
# # data = pd.read_csv('data/merged_test_dataset.csv', usecols=['date', 'visits', 'cases', 'daily_cases', 'deaths', 'daily_deaths'])

# # #Transform data
# # data['date'] = pd.to_datetime(data['date'])
# # data['visits_2019'] = data.visits/1.5
# # #data = data[data['date'].dt.year == 2022]                      #filter year
# # #data['daily_cases_diff'] = data.daily_cases.diff().fillna(0)   #differences
# # #data = data[['date', 'daily_cases']]                           #relevant vars
# # # data['visits_norm'] = stats.zscore(data['visits']) # NORMALIZE TO SAME YEAR OR 2019?

# # #Layout
# # layout = go.Layout(paper_bgcolor='rgba(0,0,0,0)', 
# #                 plot_bgcolor='rgba(0,0,0,0)',
# #                 title=None,
# #                 title_font_family='Times New Roman',
# #                 title_font_color=None,
# #                 font_family='Arial',
# #                 font_color=None,
# #                 yaxis_title=None, 
# #                 xaxis_title=None) #,
# #                 # annotations=d)
# #                 # xaxis = go.layout.XAxis(showticklabels=False),
# #                 # yaxis = go.layout.YAxis(title=None))

# # # trace_2021 = go.Scatter(
# # #     x = data['date'], 
# # #     y = data['visits'], 
# # #     mode='lines',
# # #     name="2021",
# # #     line=dict(shape='linear', color='#1C86EE', dash='solid')
# # # )

# # # trace_2019 = go.Scatter(
# # #     x = data['date'], 
# # #     y = data['visits_2019'], 
# # #     mode='lines',
# # #     name="2019",
# # #     line=dict(shape='linear', color="#C1CDCD", dash='dash')
# # # )

# # # trace_diff = go.Scatter(
# # #     x = data['date'], 
# # #     y = data['visits']-data["visits_2019"], 
# # #     mode='lines',
# # #     name="Difference",
# # #     line=dict(shape='linear', color='red', dash='solid')
# # # )

# # # layout = dict(
# # #     paper_bgcolor='rgba(0,0,0,0)', 
# # #     plot_bgcolor='rgba(0,0,0,0)',
# # #     title="Daily visits to government websites (in millions)",
# # #     title_font_family='Times New Roman',
# # #     title_font_color=None,
# # #     font_family='Arial',
# # #     font_color=None,
# # #     yaxis_title=None, 
# # #     xaxis_title=None
# # # )

# # # data = [trace_2021, trace_2019, trace_diff]
# # # fig = go.Figure(data=data, layout=layout)
# # # fig.show()

# # #Create visualization
# # fig = make_subplots(rows=2, 
# #                     cols=1,
# #                     x_title=None,
# #                     y_title=None,
# #                     # shared_xaxes=True,
# #                     subplot_titles=None)

# # #Government website visits (transform visits to weekly to avoid weekend drops)
# # #2021
# # fig.add_trace(go.Scatter(x = data['date'], 
# #                          y = data['visits'], 
# #                          mode='lines',
# #                          name="2021",
# #                          line=dict(shape='linear', color='#1E90FF', dash='solid')),
# #               row=1, col=1)
# # #2019
# # fig.add_trace(go.Scatter(x = data['date'], 
# #                          y = data['visits_2019'], 
# #                          mode='lines',
# #                          name="Baseline (2019)",
# #                          line=dict(shape='linear', color="#C1CDCD", dash='dash')), 
# #               row=1, col=1)
# # #Difference
# # fig.add_trace(go.Scatter(x = data['date'], 
# #                          y = data['visits']-data["visits_2019"], 
# #                          mode='lines',
# #                          name="Difference",
# #                          line=dict(shape='linear', color='#CD2626', dash='solid')), #3D9140 #CD2626
# #               row=1, col=1)

# # fig.update_layout(layout)
# # fig.update_xaxes(showticklabels=False)
# # fig.update_yaxes(gridcolor="#eee", griddash="solid", gridwidth=0.5, 
# #                 range=[0, max(max(data['visits']), max(data['visits_2019']))+3000000])

# # #Add events
# # event_1 = {'year': 2021, 'month': 3, 'day': 13, 'event': 'Event 1'} 
# # event_2 = {'year': 2021, 'month': 7, 'day': 2, 'event': 'Event 2'} 
# # event_3 = {'year': 2021, 'month': 11, 'day': 29, 'event': 'Event 3'} 
# # events = [event_1, event_2, event_3]

# # for event in events:
# #     fig.add_vline(x=datetime.datetime(
# #                     event['year'],event['month'],event['day']).timestamp()*1000, 
# #                     line_width=1, 
# #                     line_dash="solid", 
# #                     line_color="red", 
# #                     annotation_text=event['event'])

