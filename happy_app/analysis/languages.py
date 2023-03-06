import pandas as pd
from dash import dcc
import plotly.express as px
import plotly.graph_objects as go

data = pd.read_csv('happy_app/data/update_data/language.csv', usecols=['language_name', 'visits'])
data = data.groupby('language_name').sum()

Label_per = [str(round(i*100/sum(df_coal.Value),1))+' %' for i in df_coal.Value]
import plotly.express as px
fig = px.treemap(df_coal, path=[px.Constant('2022'), 'Country'],
                 values=df_coal.Percent,
                 color=df_coal.Country,
                 color_discrete_map=color_country,
                 hover_name=Label_per,
                )
fig.update_layout(margin = dict(t=50, l=25, r=25, b=25), showlegend=True)
fig.show()
