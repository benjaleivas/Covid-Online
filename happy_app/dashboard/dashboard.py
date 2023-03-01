# import numpy as np
# import pandas as pd
# from dash import dcc
# from scipy import stats
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots



# #Load merged data
# data = pd.read_csv('data/merged_test_dataset.csv', usecols=['date', 'visits', 'cases', 'daily_cases', 'deaths', 'daily_deaths'])

# #Transform data
# data['date'] = pd.to_datetime(data['date'])
# data['visits_2019'] = data.visits/1.5

# #Layout
# layout = go.Layout(paper_bgcolor='rgba(0,0,0,0)', 
#                 plot_bgcolor='rgba(0,0,0,0)',
#                 title="Daily visits to government websites (in millions)",
#                 title_font_family='Times New Roman',
#                 title_font_color=None,
#                 font_family='Arial',
#                 font_color=None,
#                 yaxis_title=None, 
#                 xaxis_title=None)

# #Create visualization
# fig = make_subplots(rows=2, 
#                     cols=1,
#                     x_title=None,
#                     y_title=None,
#                     # shared_xaxes=True,
#                     subplot_titles=None)

# #Government website visits (transform visits to weekly to avoid weekend drops)
# #2021
# fig.add_trace(go.Scatter(x = data['date'], 
#                          y = data['visits'], 
#                          mode='lines',
#                          name="2021",
#                          line=dict(shape='linear', color='#1C86EE', dash='solid')),
#               row=1, col=1)
# #2019
# fig.add_trace(go.Scatter(x = data['date'], 
#                          y = data['visits_2019'], 
#                          mode='lines',
#                          name="2019",
#                          line=dict(shape='linear', color="#C1CDCD", dash='dash')), 
#               row=1, col=1)
# #Difference
# fig.add_trace(go.Scatter(x = data['date'], 
#                          y = data['visits']-data["visits_2019"], 
#                          mode='lines',
#                          name="Difference",
#                          line=dict(shape='linear', color='red', dash='solid')),
#               row=1, col=1)

# fig.update_layout(layout)
# fig.update_xaxes(showticklabels=False)
# fig.update_yaxes(gridcolor="#eee", griddash="solid", gridwidth=0.5, 
#                 range=[0, max(max(data['visits']), max(data['visits_2019']))+3000000])

# #fig.show()

# graph = dcc.Graph(id='visits_trend', figure=fig)
# dcc.Download(id='visits_trend')



import dash
import pandas as pd
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go

from happy_app.analysis.websites_visits import visits_vs_2019
# from analysis.websites_visits import visits_vs_2019


#import 


graph_20210_2020 = visits_vs_2019(2020)

#from analysis.websites_visits import weekly_visits_vs_2019


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])




def generate_title_container(title_text, subtitle_text):
    title_container = dbc.Container(
        fluid=True,
        style={
            "height": "100vh",
            "background-color": "#005aae",
            "color": "white",
            "display": "flex",
            "flex-direction": "column",
            "justify-content": "center",
            "align-items": "center"
        },
        children=[
            html.H1(title_text, style={"font-size": "8rem", "text-align": "center"}),
            html.Br(),
            html.Br(),
            html.H2(subtitle_text, style={"font-size": "1rem", "text-align": "center"}),
            html.Br(),
            html.Br(),
            dbc.Row(
                dbc.Col(
                    html.Button("Scroll Down", id="scroll-down-button", className="btn btn-primary", style={"background-color": "white", "color": "#005aae"}),
                    width=12,
                    style={"display": "flex", "justify-content": "center", "align-items": "flex-end", "padding-bottom": "4rem"}
                )
            )
        ]
    )
    return title_container


def generate_subtitle_container(subtitle_text, background_color, text_color ):
    subtitle_container = dbc.Container(
        fluid=True,
        style={
            "height": "20vh",
            "background-color": background_color,
            "color": text_color,
            "display": "flex",
            "flex-direction": "column",
            "justify-content": "center",
            "align-items": "flex-start"
        },
        children=[
            dbc.Row(
                dbc.Col(
                    html.H1(subtitle_text, style={"font-size": "3rem"}),
                    width=12,
                    style={"display": "flex", "justify-content": "center", "align-items": "center"}
                )
            )
        ]
    )
    return subtitle_container


def generate_graph_container_one(title_text, paragraph_text, graph_component, title_color):
    graph_container = dbc.Container(
        fluid=True,
        children=[
            dbc.Row([
                dbc.Col([
                    html.H1(title_text, style={"text-align": "left", "color": title_color, "font-size": "3rem"}),
                    html.P(paragraph_text, style={"font-size": "1rem"})
                ], width=4),
                dbc.Col([
                    html.H2("Graph Title", style={"text-align": "left", "color": title_color, "font-size": "2rem"}),
                    graph_component, 
                ], width=8)
            ])
        ]
    )
    return graph_container






def generate_graph_container_two(title_text, paragraph_text, graph_component, 
                                 graph_component_2, title_color):
    graph_container = dbc.Container(
        fluid=True,
        children=[
            dbc.Row([
                dbc.Col([
                    html.H1(title_text, style={"text-align": "left", "color": title_color, "font-size": "3rem"}),
                    html.P(paragraph_text, style={"font-size": "1rem"})
                ], width=4),
                dbc.Col([
                    html.H2("Graph Title", style={"text-align": "left", "color": title_color, "font-size": "2rem"}),
                    graph_component, 
                    graph_component_2
                ], width=8)
            ])
        ]
    )
    return graph_container

import dash_core_components as dcc

def generate_graph_container_interactive(title_text, paragraph_text, graph_component_1, graph_component_2, graph_component_3, title_color):
    graph_container = dbc.Container(
        fluid=True,
        children=[
            dbc.Row([
                dbc.Col([
                    html.H1(title_text, style={"text-align": "left", "color": title_color, "font-size": "3rem"}),
                    html.P(paragraph_text, style={"font-size": "1rem"})
                ], width=4),
                dbc.Col([
                    html.H2("Graph Title", style={"text-align": "left", "color": title_color, "font-size": "2rem"}),
                    dcc.Dropdown(
                        id='graph-dropdown',
                        options=[
                            {'label': 'Graph 1', 'value': 'graph1'},
                            {'label': 'Graph 2', 'value': 'graph2'},
                            {'label': 'Graph 3', 'value': 'graph3'}
                        ],
                        value='graph1'
                    ),
                    html.Div(
                        id='graph-container',
                        children=graph_component_1
                    )
                ], width=8)
            ])
        ]
    )
    return graph_container

def generate_numbers_container(title_text, paragraph_text, number1, explanation1, number2, explanation2, title_color='black', number_color='black'):
    container = dbc.Container(
        fluid=True,
        style={'height': '50vh'},
        children=[
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H1(title_text, style={"color": title_color, "font-size": "4rem"}),
                            html.P(paragraph_text)
                        ],
                        width=4,
                        style={'height': '40vh', 'display': 'flex', 'flex-direction': 'column', 'justify-content': 'center'}
                    ),
                    dbc.Col(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.H1(f"{number1}%", style={'text-align': 'center', 'font-size': '6rem', 'color': number_color}),
                                            html.P(explanation1, style={'text-align': 'center'})
                                        ],
                                        width=6,
                                        style={'display': 'flex', 'flex-direction': 'column', 'justify-content': 'center'}
                                    ),
                                    dbc.Col(
                                        [
                                            html.H1(f"{number2}%", style={'text-align': 'center', 'font-size': '6rem', 'color': number_color}),
                                            html.P(explanation2, style={'text-align': 'center'})
                                        ],
                                        width=6,
                                        style={'display': 'flex', 'flex-direction': 'column', 'justify-content': 'center'}
                                    )
                                ],
                                style={'height': '50%'}
                            )
                        ],
                        width=8,
                        style={'display': 'flex', 'flex-direction': 'column', 'justify-content': 'space-between'}
                    )
                ],
                style={'height': '100%'}
            )
        ]
    )
    return container

import dash_bootstrap_components as dbc

def generate_conclusion_container(title_text, list_items, bg_color):
    container = dbc.Container(
        fluid=True,
        style={'height': '100vh', 'background-color': bg_color},
        children=[
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H1(title_text, style={'color': 'white', 'font-size': '5rem', 'margin-bottom': '2rem', 'text-align': 'center'}),
                            html.Ul(
                                [html.Li(item, style={'color': 'white', 'font-size': '2rem', 'text-align': 'center'}) for item in list_items],
                                style={'list-style-type': 'none', 'padding-left': '0', 'margin-top': '2rem', 'text-align': 'center'}
                            )
                        ],
                        width=12,
                        style={'display': 'flex', 'flex-direction': 'column', 'justify-content': 'center', 'align-items': 'center'}
                    )
                ],
                style={'height': '100%'}
            )
        ]
    )
    return container










# def generate_graph_container_two(title_left, title_right, graph_component_left, graph_component_right, title_color):
#     graph_container = dbc.Container(
#         fluid=True,
#         children=[
#             dbc.Row([
#                 dbc.Col([
#                     html.H1(title_left, style={"text-align": "left", "color": title_color, "font-size": "3rem"}),
#                     graph_component_left
#                 ], width=4),
#                 dbc.Col([                    html.H1(title_right, style={"text-align": "left", "color": title_color, "font-size": "3rem"}),                    graph_component_right                ], width=8)
#             ])
#         ]
#     )
#     return graph_container









# def generate_graph_container_two(title_text, paragraph_text, title_color):
#     # Define the two graph components
#     graph_left = dcc.Graph(figure={"data": [{"x": [1, 2, 3], "y": [1, 2, 3], "type": "scatter", "mode": "lines"}]})
#     graph_right = dcc.Graph(figure={"data": [{"x": ["A", "B", "C"], "y": [3, 2, 1], "type": "bar"}]})

#     # Define the layout of the container
#     graph_container = dbc.Container(
#         fluid=True,
#         children=[
#             dbc.Row(
#                 dbc.Col(
#             html.H1(title_text, style={"text-align": "left", "color": title_color, "font-size": "3rem"}),
#                     width=12
#                 )
#             ),
#             html.P(paragraph_text, style={"font-size": "1rem"}),
#             dbc.Row(
#                 [
#                     dbc.Col(
#                         graph_left,
#                         width={"size": 6, "order": 1}
#                     ),
#                     dbc.Col(
#                         graph_right,
#                         width={"size": 6, "order": 2}
#                     )
#                 ]
#             )
#         ]
#     )

#     return graph_container

##############
# Fake data 
###############

# Bar plot
data = {'fruit': ['apple', 'orange', 'banana'], 'quantity': [10, 5, 20]}
df = pd.DataFrame(data)
fig_bar = go.Figure(data=[go.Bar(x=df['fruit'], y=df['quantity'])])
graph_component_bar = dcc.Graph(figure=fig_bar)

# Line plot
data = {'year': [2010, 2011, 2012, 2013, 2014, 2015, 2016],
        'sales': [100, 150, 200, 250, 300, 350, 400]}
df = pd.DataFrame(data)
fig_line = go.Figure(data=[go.Scatter(x=df['year'], y=df['sales'], mode='lines')])
graph_component_line = dcc.Graph(figure=fig_line)

# Treemap
data = px.data.gapminder().query("year == 2007").query("continent == 'Asia'")
fig_treemap = px.treemap(data, path=['continent', 'country'], values='pop',
                         color='lifeExp', hover_data=['iso_alpha'])
graph_component_treemap = dcc.Graph(figure=fig_treemap)





title_container = generate_title_container("COVID-19 Online:",
 "How were people interacting with COVID-19 goverment pages during the crisis?")
subtitle_container_goverment_pages = generate_subtitle_container("WERE WE USING GOVERMENT PAGES?",
 "#005aae", 
 "white"  )
graph_component = dcc.Graph(figure={"data": [{"y": [1, 2, 3]}]})
graph_container_cdc_data = generate_graph_container_two(
 title_text =   "CDC Data",
 paragraph_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum ac pulvinar lectus, in efficitur ligula. Nulla facilisi. Donec nec est porttitor, malesuada odio quis, lobortis velit. Fusce finibus ullamcorper nulla, et tincidunt lectus porttitor sed. Vivamus dictum dictum eleifend.",
  graph_component = graph_20210_2020, 
  graph_component_2 = graph_component_line, 
  title_color = "#808080")

# graph_container_covid_data = generate_graph_container_one(
# title_text = "COVID-19 data:", 
# paragraph_text =  "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum ac pulvinar lectus, in efficitur ligula. Nulla facilisi. Donec nec est porttitor, malesuada odio quis, lobortis velit. Fusce finibus ullamcorper nulla, et tincidunt lectus porttitor sed. Vivamus dictum dictum eleifend." , 
# graph_component = graph_component, 
# title_color = "#808080")

subtitle_container_forms_of_accesing = generate_subtitle_container(
  subtitle_text =  "FROM WHERE WERE PEOPLE ACCESING GOV. WEBSITES?",
 background_color = "#005aae", 
 text_color = "white"  )


graph_container_traffic_source = generate_graph_container_one(
title_text = "Traffic Source", 
paragraph_text =  "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum ac pulvinar lectus, in efficitur ligula. Nulla facilisi. Donec nec est porttitor, malesuada odio quis, lobortis velit. Fusce finibus ullamcorper nulla, et tincidunt lectus porttitor sed. Vivamus dictum dictum eleifend." , 
graph_component = graph_component_bar, 
title_color = "#808080")

numbers_container = generate_numbers_container(
    title_text = "Numbers",
    paragraph_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum ac pulvinar lectus, in efficitur ligula. Nulla facilisi. Donec nec est porttitor, malesuada odio quis, lobortis velit. Fusce finibus ullamcorper nulla, et tincidunt lectus porttitor sed. Vivamus dictum dictum eleifend.", 
    number1 = 60, 
    explanation1 = "Number of cases", 
    number2 = 40, 
    explanation2 = "Number of cases", 
    title_color= "#808080", 
    number_color= "#005aae")

subtitle_container_language = generate_subtitle_container(
  subtitle_text =  "DID USER LANGUAGE PLAYED A ROLE?",
 background_color = "#005aae", 
 text_color = "white"  )

graph_container_language = generate_graph_container_interactive(
    title_text = "Attemp for interactive graph", 
    paragraph_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum ac pulvinar lectus, in efficitur ligula. Nulla facilisi. Donec nec est porttitor, malesuada odio quis, lobortis velit. Fusce finibus ullamcorper nulla, et tincidunt lectus porttitor sed. Vivamus dictum dictum eleifend.", 
    graph_component_1 = graph_component_treemap, 
    graph_component_2 = graph_component_line, 
    graph_component_3 = graph_component_bar, 
    title_color = "#808080")

subtitle_container_most_visited_pages = generate_subtitle_container(
  subtitle_text =  "WHICH WERE THE PAGES THE USERS USED THE MOST?", 
 background_color = "#005aae", 
 text_color = "white"  )

conclusion_container = generate_conclusion_container(
        title_text="Conclusion",
        list_items=[
            "1. This is our first conclusion.",
            "2. This is our second conclusion.",
            "3. This is our third conclusion."
        ],
        bg_color="#005aae"
    )





# subtitle_container_disease = generate_subtitle_container("How were the main COVID-19 indicators?", 
#  "#005aae", 
#  "white"  )
# graph_container_disease = generate_graph_container_one("Unemployment",
#  "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum ac pulvinar lectus, in efficitur ligula. Nulla facilisi. Donec nec est porttitor, malesuada odio quis, lobortis velit. Fusce finibus ullamcorper nulla, et tincidunt lectus porttitor sed. Vivamus dictum dictum eleifend.",
#   graph_component, 
#   "#00ACC7")
# covid_data = generate_graph_container_two("How were the main COVID-19 indicators?",
#  "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum ac pulvinar lectus, in efficitur ligula. Nulla facilisi. Donec nec est porttitor, malesuada odio quis, lobortis velit. Fusce finibus ullamcorper nulla, et tincidunt lectus porttitor sed. Vivamus dictum dictum eleifend.", 
#  "#005aae")

app.layout = html.Div(children=[
    title_container,
    subtitle_container_goverment_pages,
    graph_container_cdc_data, 
    #graph_container_covid_data, 
    subtitle_container_forms_of_accesing, 
    graph_container_traffic_source, 
    numbers_container, 
    subtitle_container_language, 
    graph_container_language, 
    subtitle_container_most_visited_pages, 
    graph_container_traffic_source, 
    conclusion_container

    #subtitle_container_disease, 
    #covid_data
])


@app.callback(
    dash.dependencies.Output('graph-container', 'children'),
    [dash.dependencies.Input('graph-dropdown', 'value')]
)

def update_graph_container(value):
    if value == 'graph1':
        return graph_component_bar 
    elif value == 'graph2':
        return graph_component_line
    elif value == 'graph3':
        return graph_component_treemap 


# Run app
if __name__=='__main__':
    app.run_server(port=8051)
