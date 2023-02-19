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

# Build components
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
mytext = dcc.Markdown(children="# Are Americans Looking to .gov Websites for Health Information?")
myparagraph = dbc.Row([
    dbc.Col(html.P("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum ac pulvinar lectus, in efficitur ligula. Nulla facilisi. Donec nec est porttitor, malesuada odio quis, lobortis velit. Fusce finibus ullamcorper nulla, et tincidunt lectus porttitor sed. Vivamus dictum dictum eleifend. Cras nec nunc at lectus ornare posuere. Praesent tempor porta erat, et finibus risus. In et ornare enim. Aliquam erat volutpat. Integer viverra augue vitae erat ultricies gravida. Etiam pellentesque ipsum in tortor finibus porttitor."), width=10)
])

# Get the data
df = get_data()

# Add time series graph
fig = {
    'data': [
        {'x': df['date'], 'y': df['unemployment_rate'], 'type': 'line', 'name': 'Value'},
    ],
    'layout': {
        'title': 'Time Series Graph',
        'xaxis': {'title': 'Date'},
        'yaxis': {'title': 'Value'}
    }
}
mygraph = dcc.Graph(figure=fig)

# Customize your own Layout
app.layout = dbc.Container([
    mytext,
    myparagraph, 
    mygraph
])

# Run app
if __name__=='__main__':
    app.run_server(port=8051)