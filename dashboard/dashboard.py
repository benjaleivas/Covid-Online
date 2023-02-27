import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from analysis.websites_visits import graph 

#from .analysis import websites_visits.graph 


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
                    graph_component
                ], width=8)
            ])
        ]
    )
    return graph_container

def generate_graph_container_two(title_left, title_right, graph_component_left, graph_component_right, title_color):
    graph_container = dbc.Container(
        fluid=True,
        children=[
            dbc.Row([
                dbc.Col([
                    html.H1(title_left, style={"text-align": "left", "color": title_color, "font-size": "3rem"}),
                    graph_component_left
                ], width=4),
                dbc.Col([                    html.H1(title_right, style={"text-align": "left", "color": title_color, "font-size": "3rem"}),                    graph_component_right                ], width=8)
            ])
        ]
    )
    return graph_container









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


# Example usage of the functions

title_container = generate_title_container("COVID-19 Online:",
 "How were people interacting with COVID-19 goverment pages during the crisis?")
subtitle_container_goverment_pages = generate_subtitle_container("WERE WE USING GOVERMENT PAGES?",
 "#005aae", 
 "white"  )
graph_component = dcc.Graph(figure={"data": [{"y": [1, 2, 3]}]})
graph_container_cdc_data = generate_graph_container_one("CDC Data",
 "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum ac pulvinar lectus, in efficitur ligula. Nulla facilisi. Donec nec est porttitor, malesuada odio quis, lobortis velit. Fusce finibus ullamcorper nulla, et tincidunt lectus porttitor sed. Vivamus dictum dictum eleifend.",
  graph, 
  "#808080")
graph_container_covid_data = generate_graph_container_one(
title_text = "COVID-19 data:", 
paragraph_text =  "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum ac pulvinar lectus, in efficitur ligula. Nulla facilisi. Donec nec est porttitor, malesuada odio quis, lobortis velit. Fusce finibus ullamcorper nulla, et tincidunt lectus porttitor sed. Vivamus dictum dictum eleifend." , 
graph_component = graph_component, 
title_color = "#808080")

subtitle_container_forms_of_accesing = generate_subtitle_container(
  subtitle_text =  "FROM WHERE WERE PEOPLE ACCESING GOV. WEBSITES?",
 background_color = "#005aae", 
 text_color = "white"  )
graph_container_traffic_source = generate_graph_container_one(
title_text = "Traffic Source", 
paragraph_text =  "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum ac pulvinar lectus, in efficitur ligula. Nulla facilisi. Donec nec est porttitor, malesuada odio quis, lobortis velit. Fusce finibus ullamcorper nulla, et tincidunt lectus porttitor sed. Vivamus dictum dictum eleifend." , 
graph_component = graph_component, 
title_color = "#808080")





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
    graph_container_covid_data, 
    subtitle_container_forms_of_accesing, 
    graph_container_traffic_source
    #subtitle_container_disease, 
    #covid_data
])

# Run app
if __name__=='__main__':
    app.run_server(port=8051)
