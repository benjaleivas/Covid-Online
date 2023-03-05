import dash
from dash import dcc
from dash import html
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

from happy_app.analysis.hhs_visits import plot_hhs_visits
from happy_app.analysis.covid_cases import plot_covid_cases





app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

#En caso de que querramos quedarnos con la versión anterior 
# def generate_title_container(title_text, subtitle_text):
#     title_container = dbc.Container(
#         fluid=True,
#         style={
#             "height": "100vh",
#             "background-color": "#005aae",
#             "color": "white",
#             "display": "flex",
#             "flex-direction": "column",
#             "justify-content": "center",
#             "align-items": "center"
#         },
#         children=[
#             html.H1(title_text, style={"font-size": "8rem", "text-align": "center"}),
#             html.Br(),
#             html.Br(),
#             html.H2(subtitle_text, style={"font-size": "1rem", "text-align": "center"}),
#             html.Br(),
#             html.Br(),
#             dbc.Row(
#                 dbc.Col(
#                     html.Button("Scroll Down", id="scroll-down-button", className="btn btn-primary", style={"background-color": "white", "color": "#005aae"}),
#                     width=12,
#                     style={"display": "flex", "justify-content": "center", "align-items": "flex-end", "padding-bottom": "4rem"}
#                 )
#             )
#         ]
#     )
#     return title_container

def generate_title_container(title_text, subtitle_text, subtitle_list, subtitles_id):
    subtitle_buttons = []
    for i, subtitle in enumerate(subtitle_list):
        subtitle_id = subtitles_id[i] if subtitles_id else f"subtitle-{i}"
        subtitle_buttons.append(
            dbc.Col(
                dcc.Link(
                    dbc.Button(subtitle, color="primary", id=f"{subtitle}-button", style={"background-color": "#00ACC7", "color": "white"}),
                    href=f"#{subtitle_id}"
                ),
                width=4,
                style={"display": "flex", "justify-content": "center", "margin-bottom": "1rem", "background-color": "#005aae"}
            )
        )
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
            html.H2(subtitle_text, style={"font-size": "2rem", "text-align": "center"}),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            dbc.Row(
                subtitle_buttons,
                style={"display": "flex", "justify-content": "center"}
            )
        ]
    )
    return title_container



def generate_subtitle_container(subtitle_text, background_color, text_color, subtitle_id):
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
        id=subtitle_id,  # Add an ID attribute to the container
        children=[
            dbc.Row(
                dbc.Col(
                    html.A(html.H1(subtitle_text, style={"font-size": "3rem", "color": "white"}),
                    href=f"#{subtitle_id}"),  # Add an anchor link to the container
                    width=12,
                    style={"display": "flex", "justify-content": "center", "align-items": "center"}
                )
            )
        ]
    )
    return subtitle_container

# def generate_subtitle_container(subtitle_text, background_color, text_color ):
#     subtitle_container = dbc.Container(
#         fluid=True,
#         style={
#             "height": "20vh",
#             "background-color": background_color,
#             "color": text_color,
#             "display": "flex",
#             "flex-direction": "column",
#             "justify-content": "center",
#             "align-items": "flex-start"
#         },
#         children=[
#             dbc.Row(
#                 dbc.Col(
#                     html.H1(subtitle_text, style={"font-size": "3rem"}),
#                     width=12,
#                     style={"display": "flex", "justify-content": "center", "align-items": "center"}
#                 )
#             )
#         ]
#     )
#     return subtitle_container


def generate_graph_container_one(title_text, paragraph_text, graph_component, title_color):
    graph_container = dbc.Container(
        fluid=True,
        children=[
            dbc.Row([
                dbc.Col([
                    html.H1(title_text, style={"text-align": "left", "color": title_color, "font-size": "2rem"}),
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
                    html.H1(title_text, style={"text-align": "left", "color": title_color, "font-size": "2rem"}),
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




def generate_numbers_container(title_text, paragraph_text, number1, explanation1, number2, explanation2, number3, explanation3, title_color='black', number_color='black'):
    container = dbc.Container(
        fluid=True,
        style={'height': '50vh'},
        children=[            dbc.Row(                [                    dbc.Col(                        [                            html.H1(title_text, style={"color": title_color, "font-size": "2rem"}),                            html.P(paragraph_text)                        ],
                        width=4,
                        style={'height': '40vh', 'display': 'flex', 'flex-direction': 'column', 'justify-content': 'center'}
                    ),
                    dbc.Col(
                        [                            dbc.Row(                                [                                    dbc.Col(                                        [                                            html.H1(f"{number1}%", style={'text-align': 'center', 'font-size': '6rem', 'color': number_color}),                                            html.P(explanation1, style={'text-align': 'center'})                                        ],
                                        width=4,
                                        style={'display': 'flex', 'flex-direction': 'column', 'justify-content': 'center'}
                                    ),
                                    dbc.Col(
                                        [                                            html.H1(f"{number2}%", style={'text-align': 'center', 'font-size': '6rem', 'color': number_color}),                                            html.P(explanation2, style={'text-align': 'center'})                                        ],
                                        width=4,
                                        style={'display': 'flex', 'flex-direction': 'column', 'justify-content': 'center'}
                                    ),
                                    dbc.Col(
                                        [                                            html.H1(f"{number3}%", style={'text-align': 'center', 'font-size': '6rem', 'color': number_color}),                                            html.P(explanation3, style={'text-align': 'center'})                                        ],
                                        width=4,
                                        style={'display': 'flex', 'flex-direction': 'column', 'justify-content': 'center'}
                                    ),
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

def generate_graph_container_interactive(title_text, paragraph_text, graph_component_1, graph_component_2, graph_component_3, title_color):
    graph_container = dbc.Container(
        fluid=True,
        children=[
            dbc.Row([
                dbc.Col([
                    html.H1(title_text, style={"text-align": "left", "color": title_color, "font-size": "2rem"}),
                    html.P(paragraph_text, style={"font-size": "1rem"})
                ], width=4),
                dbc.Col([
                    html.H2("Graph Title", style={"text-align": "left", "color": title_color, "font-size": "2rem"}),
                    dcc.Dropdown(
                        id='graph-dropdown-2',
                        options=[
                            {'label': 'Graph 1', 'value': 'graph1'},
                            {'label': 'Graph 2', 'value': 'graph2'},
                            {'label': 'Graph 3', 'value': 'graph3'}
                        ],
                        value='graph1'
                    ),
                    html.Div(
                        id='graph-container-2',
                        children=graph_component_1
                    )
                ], width=8)
            ])
        ]
    )
    return graph_container

def generate_graph_container_interactive_two(title_text, paragraph_text, graph_component_1, graph_component_2, graph_component_3, graph_component_4, graph_component_5, graph_component_6, title_color):
    graph_container = dbc.Container(
        fluid=True,
        children=[
            dbc.Row([
                dbc.Col([
                    html.H1(title_text, style={"text-align": "left", "color": title_color, "font-size": "2rem"}),
                    html.P(paragraph_text, style={"font-size": "1rem"})
                ], width=4),
                dbc.Col([
                    html.H2("Graph Title", style={"text-align": "left", "color": title_color, "font-size": "2rem"}),
                    dcc.Dropdown(
                        id='graph-dropdown-1',
                        options=[
                            {'label': 'Graph 1', 'value': 'graph1'},
                            {'label': 'Graph 2', 'value': 'graph2'},
                            {'label': 'Graph 3', 'value': 'graph3'}
                        ],
                        value='graph1'
                    ),
                    html.Div(
                        id='graph-container-1',
                        children=[graph_component_1, graph_component_2]
                    )
                ], width=8)
            ])
        ]
    )
    return graph_container



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




subtitle_list = ["Covid and Gov Pages", 
                 "Forms of accesing", 
                 "Language", 
                 "Most visited pages"]

subtitles_id = ["gov_pages", 
                "forms_accesing", 
                "language", 
                "most_used"
                ]

title_container = generate_title_container(
    "COVID-19 Online:", 
    "How were people interacting with COVID-19 goverment pages during the crisis?", 
    subtitle_list, 
    subtitles_id)


# title_container = generate_title_container("COVID-19 Online:",
#  "How were people interacting with COVID-19 goverment pages during the crisis?")
subtitle_container_goverment_pages = generate_subtitle_container(
    subtitle_text = "WERE WE USING GOVERMENT PAGES?",
 background_color = "#005aae", 
   text_color = "white", 
   subtitle_id = "gov_pages"
     )


graph_container_cdc_data = generate_graph_container_two(
 title_text =   "CDC Data",
 paragraph_text = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. Nam quam nunc, blandit vel, luctus pulvinar, hendrerit id, lorem. Maecenas nec odio et ante tincidunt tempus. Donec vitae sapien ut libero venenatis faucibus. Nullam quis ante. Etiam sit amet orci eget eros faucibus tincidunt. Duis leo. Sed fringilla mauris sit amet nibh. Donec sodales sagittis magna. Sed consequat, leo eget bibendum sodales, augue velit cursus nunc.",
  graph_component = graph_component_bar, 
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
 text_color = "white", 
subtitle_id = "forms_accesing" )



graph_container_traffic_source = generate_graph_container_one(
title_text = "Traffic Source", 
paragraph_text =  "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum ac pulvinar lectus, in efficitur ligula. Nulla facilisi. Donec nec est porttitor, malesuada odio quis, lobortis velit. Fusce finibus ullamcorper nulla, et tincidunt lectus porttitor sed. Vivamus dictum dictum eleifend." , 
graph_component = graph_component_bar, 
title_color = "#808080")

numbers_container = generate_numbers_container(
    title_text = "Numbers",
    paragraph_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum ac pulvinar lectus, in efficitur ligula. Nulla facilisi. Donec nec est porttitor, malesuada odio quis, lobortis velit. Fusce finibus ullamcorper nulla, et tincidunt lectus porttitor sed. Vivamus dictum dictum eleifend.", 
    number1 = 33.3, 
    explanation1 = "Number of cases", 
    number2 = 33.3, 
    explanation2 = "Number of cases", 
    number3 = 33.3, 
    explanation3 = "Number of cases", 
    title_color= "#808080", 
    number_color= "#005aae")

subtitle_container_language = generate_subtitle_container(
  subtitle_text =  "DID USER LANGUAGE PLAYED A ROLE?",
 background_color = "#005aae", 
 text_color = "white", 
 subtitle_id = "language")

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
 text_color = "white", 
   subtitle_id = "most_used"  )

conclusion_container = generate_conclusion_container(
        title_text="Conclusion",
        list_items=[
            "1. This is our first conclusion.",
            "2. This is our second conclusion.",
            "3. This is our third conclusion."
        ],
        bg_color="#005aae"
    )

#import graphs 
graph_2019_2020 = plot_hhs_visits(2020)
graph_2019_2021 = plot_hhs_visits(2021)
graph_2019_2022 = plot_hhs_visits(2022)

graph_covid_2020 = plot_covid_cases(2020, "daily_cases")

interactive_two_container = generate_graph_container_interactive_two(
    title_text = "Attemp for interactive graph", 
    paragraph_text = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. Nam quam nunc, blandit vel, luctus pulvinar, hendrerit id, lorem. Maecenas nec odio et ante tincidunt tempus. Donec vitae sapien ut libero venenatis faucibus. Nullam quis ante. Etiam sit amet orci eget eros faucibus tincidunt. Duis leo. Sed fringilla mauris sit amet nibh. Donec sodales sagittis magna. Sed consequat, leo eget bibendum sodales, augue velit cursus nunc.", 
    graph_component_1 = graph_2019_2020 , 
    graph_component_2 = graph_covid_2020, 
    graph_component_3 = graph_2019_2021, 
    graph_component_4 = graph_component_bar, 
    graph_component_5 = graph_2019_2022, 
    graph_component_6 = graph_component_bar, 
    title_color = "#005aae") 
   





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
    interactive_two_container,
    #graph_container_cdc_data, 
    #graph_container_covid_data, 
    subtitle_container_forms_of_accesing, 
    graph_container_traffic_source, 
    numbers_container, 
    subtitle_container_language, 
    graph_container_language, 
    subtitle_container_most_visited_pages, 
    graph_container_cdc_data, 
    conclusion_container

    #subtitle_container_disease, 
    #covid_data
])


@app.callback(
    [dash.dependencies.Output('graph-container-1', 'children'),
     dash.dependencies.Output('graph-container-2', 'children')],
    [dash.dependencies.Input('graph-dropdown-1', 'value'),
     dash.dependencies.Input('graph-dropdown-2', 'value')]
)

def update_graph_container(value1, value2):
    if value1 == 'graph1':
        graph_container_1 = [graph_2019_2020, graph_covid_2020]
    elif value1 == 'graph2':
        graph_container_1 = [graph_2019_2021, graph_component_bar]
    elif value1 == 'graph3':
        graph_container_1 = [graph_2019_2022, graph_component_line]
    
    if value2 == 'graph1':
        graph_container_2 = graph_component_bar 
    elif value2 == 'graph2':
        graph_container_2 = graph_component_line
    elif value2 == 'graph3':
        graph_container_2 = graph_component_treemap
    
    return graph_container_1, graph_container_2





# Run app
if __name__=='__main__':
    app.run_server(port=8051)