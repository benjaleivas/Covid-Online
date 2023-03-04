import pandas as pd
# from dash import dcc
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_domain_visits(domain, year):
    """
    Plots domain visits for year and relative percentage for all HHS websites.

    Input:
        - domain (str): name of the domain
        - year (int): year to plot
    
    Returns (object): DCC Graph.
    """
    #Load data
    data2019 = pd.read_csv('happy_app/data/update_data/2019_second-level-domain_by_week.csv')