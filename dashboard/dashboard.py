import pathlib
from dash import Dash, dcc, Output, Input  # pip install dash
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
import pandas as pd                        # pip install pandas
import dash_html_components as html

# incorporate data into app

def get_data ():

    csv_file = '../data/cleaned_bls_data.csv'

# Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)
    return df 

# Build your components
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
mytext_1 = dcc.Markdown(children="# How was unemployment during covid?", style={"color": "#005aae"})
myparagraph_1 = dbc.Row([
    dbc.Col(html.P("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum ac pulvinar lectus, in efficitur ligula. Nulla facilisi. Donec nec est porttitor, malesuada odio quis, lobortis velit. Fusce finibus ullamcorper nulla, et tincidunt lectus porttitor sed. Vivamus dictum dictum eleifend. Cras nec nunc at lectus ornare posuere. Praesent tempor porta erat, et finibus risus. In et ornare enim. Aliquam erat volutpat. Integer viverra augue vitae erat ultricies gravida. Etiam pellentesque ipsum in tortor finibus porttitor."), width=10)
])

mytext_2 = dcc.Markdown(children="# How was unemployment during covid? Barplot", style={"color": "#005aae"})
myparagraph_2 = dbc.Row([
    dbc.Col(html.P("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum ac pulvinar lectus, in efficitur ligula. Nulla facilisi. Donec nec est porttitor, malesuada odio quis, lobortis velit. Fusce finibus ullamcorper nulla, et tincidunt lectus porttitor sed. Vivamus dictum dictum eleifend. Cras nec nunc at lectus ornare posuere. Praesent tempor porta erat, et finibus risus. In et ornare enim. Aliquam erat volutpat. Integer viverra augue vitae erat ultricies gravida. Etiam pellentesque ipsum in tortor finibus porttitor."), width=10)
])
# Get the data
df = get_data()


# Add time series graph
fig1 = {
    'data': [
        {'x': df['date'], 'y': df['unemployment_rate'], 'type': 'line', 'name': 'Value'},
    ],
    'layout': {
        'title': 'Time Series Graph',
        'xaxis': {'title': 'Date'},
        'yaxis': {'title': 'Value'}
    }
}
mygraph1 = dcc.Graph(figure=fig1)

# Add barplot graph
fig2 = {
    'data': [
        {'x': df['date'], 'y': df['unemployment_rate'], 'type': 'bar', 'name': 'Value'},
    ],
    'layout': {
        'title': 'Barplot Graph',
        'xaxis': {'title': 'Date'},
        'yaxis': {'title': 'Value'}
    }
}
mygraph2 = dcc.Graph(figure=fig2)

# Customize your own Layout
# Customize your own Layout
app.layout = dbc.Container(
    fluid=True,
    children=[
        dbc.Row(
            style={
                "height": "100vh",
                "background-color": "#005aae",
                "color": "white",
                "font-size": "6rem"
            },
            children=[
                dbc.Col(
                    html.H1(
                        "Are Americans Looking to .gov Websites for Health Information?",
                        style={"text-align": "center", "font-size": "6rem", "margin-bottom": "6rem"}
                    ),
                    width=12
                ),
                dbc.Col(
                    html.H2(
                        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum ac pulvinar lectus, in efficitur ligula. Nulla facilisi. Donec nec est porttitor, malesuada odio quis, lobortis velit.",
                        style={"text-align": "center", "font-size": "1rem", "color": "#ffffff", "margin-bottom": "0.5rem"}
                    ),
                    width=12
                ),
            ],
            justify="center",
            align="center"
        ),
        mytext_1,
        myparagraph_1, 
        mygraph1, 
        mytext_2, 
        myparagraph_2, 
        mygraph2
    ]
)


# Run app
if __name__=='__main__':
    app.run_server(port=8052)