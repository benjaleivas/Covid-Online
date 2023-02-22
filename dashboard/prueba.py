import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

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
            html.H1(title_text, style={"font-size": "6rem", "text-align": "center"}),
            html.Br(),
            html.Br(),
            html.H2(subtitle_text, style={"font-size": "1rem", "text-align": "center"}),
            html.Br(),
            html.Br(),
            dbc.Row(
                dbc.Col(
                    html.Button("Scroll Down", id="scroll-down-button", className="btn btn-primary", style={"background-color": "white", "color": "#005aae"}),
                    width=12,
                    style={"display": "flex", "justify-content": "center", "align-items": "flex-end", "padding-bottom": "1rem"}
                )
            )
        ]
    )
    return title_container


def generate_subtitle_container(subtitle_text, background_color):
    subtitle_container = dbc.Container(
        fluid=True,
        style={
            "height": "100vh",
            "background-color": background_color,
            "color": "white",
            "display": "flex",
            "justify-content": "center",
            "align-items": "center"
        },
        children=[
            dbc.Row(
                dbc.Col(
                    html.H1(subtitle_text, style={"text-align": "center", "font-size": "6rem"}),
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
            html.H1(title_text, style={"text-align": "left", "color": title_color, "font-size": "3rem"}),
            html.P(paragraph_text, style={"font-size": "1rem"}),
            graph_component
        ]
    )
    return graph_container

def generate_graph_container_two(title_text, paragraph_text, title_color):
    # Define the two graph components
    graph_left = dcc.Graph(figure={"data": [{"x": [1, 2, 3], "y": [1, 2, 3], "type": "scatter", "mode": "lines"}]})
    graph_right = dcc.Graph(figure={"data": [{"x": ["A", "B", "C"], "y": [3, 2, 1], "type": "bar"}]})

    # Define the layout of the container
    graph_container = dbc.Container(
        fluid=True,
        children=[
            dbc.Row(
                dbc.Col(
            html.H1(title_text, style={"text-align": "left", "color": title_color, "font-size": "3rem"}),
                    width=12
                )
            ),
            html.P(paragraph_text, style={"font-size": "1rem"}),
            dbc.Row(
                [
                    dbc.Col(
                        graph_left,
                        width={"size": 6, "order": 1}
                    ),
                    dbc.Col(
                        graph_right,
                        width={"size": 6, "order": 2}
                    )
                ]
            )
        ]
    )

    return graph_container


# Example usage of the functions

title_container = generate_title_container("Are Americans Looking to .gov Websites for Health Information?",
 "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum ac pulvinar lectus, in efficitur ligula. Nulla facilisi. Donec nec est porttitor, malesuada odio quis, lobortis velit.")
subtitle_container_unemployment = generate_subtitle_container("How was unemployment?", "#00ACC7" )
graph_component = dcc.Graph(figure={"data": [{"y": [1, 2, 3]}]})
graph_container_unemployment = generate_graph_container_one("Unemployment",
 "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum ac pulvinar lectus, in efficitur ligula. Nulla facilisi. Donec nec est porttitor, malesuada odio quis, lobortis velit. Fusce finibus ullamcorper nulla, et tincidunt lectus porttitor sed. Vivamus dictum dictum eleifend.",
  graph_component, 
  "#005aae")
subtitle_container_disease = generate_subtitle_container("How were the main COVID-19 indicators?", "#005aae" )
graph_container_disease = generate_graph_container_one("Unemployment",
 "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum ac pulvinar lectus, in efficitur ligula. Nulla facilisi. Donec nec est porttitor, malesuada odio quis, lobortis velit. Fusce finibus ullamcorper nulla, et tincidunt lectus porttitor sed. Vivamus dictum dictum eleifend.",
  graph_component, 
  "#00ACC7")
covid_data = generate_graph_container_two("How were the main COVID-19 indicators?",
 "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum ac pulvinar lectus, in efficitur ligula. Nulla facilisi. Donec nec est porttitor, malesuada odio quis, lobortis velit. Fusce finibus ullamcorper nulla, et tincidunt lectus porttitor sed. Vivamus dictum dictum eleifend.", 
 "#005aae")

app.layout = html.Div(children=[
    title_container,
    subtitle_container_unemployment,
    graph_container_unemployment, 
    subtitle_container_disease, 
    covid_data
])

# Run app
if __name__=='__main__':
    app.run_server(port=8051)
