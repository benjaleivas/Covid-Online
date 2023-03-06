import pandas as pd
from dash import dcc
from pywaffle import Waffle
import matplotlib.pyplot as plt
import seaborn as sns

def plot_languages():
    """
    Make a waffle chart of browser language for those with over 100M visits.

    Design based on Towards Data Science Waffle Chart:
        https://towardsdatascience.com/9-visualizations-to-show-proportions-or-percentages-instead-of-a-pie-chart-4e8d81617451

    Inputs: None.

    Returns (object): DCC Graph.
    """
    #Load data
    data = pd.read_csv('happy_app/data/update_data/language.csv', 
                        usecols=['language_name', 'visits'])

    #Transform data
    data = data.groupby('language_name', as_index=False).sum()
    data['percentage'] = (data.visits / data['visits'].sum())*100
    data = data.sort_values(by='visits', ascending=False)
    data = data[data.visits > 100000000]

    #Set features for figure
    languages = data.language_name.unique()
    palette = list(sns.color_palette(palette='Paired', n_colors=len(languages)).as_hex())
    labels = [str(round(i*100/sum(data.visits),1))+' %' for i in data.visits]

    #Create figure
    fig = plt.figure(FigureClass=Waffle, 
                    rows=20, columns=50,
                    values=data.percentage, 
                    colors=palette,
                    labels=[i+' '+j for i,j in zip(data.language_name, labels)],
                    figsize = (15,6),
                    legend={'loc':'upper right',
                            'bbox_to_anchor': (1.32, 1),
                            })
    plt.tight_layout()

    return dcc.Graph(id=f'languages', figure=fig)
