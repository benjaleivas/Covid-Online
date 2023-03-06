import pandas as pd
from dash import dcc
# from pywaffle import Waffle
import plotly.express as px
import plotly.graph_objects as go

#Load data
data = pd.read_csv('happy_app/data/update_data/language.csv', usecols=['language_name', 'visits'])

#Transform data
data = data.groupby('language_name', as_index=False).sum()
data['percentage'] = (data.visits / data['visits'].sum())*100
data = data.sort_values(by='visits', ascending=False)
# data = data[data.visits > 100000000]

languages = data.language_name.unique()
labels = [str(round(i*100/sum(data.visits),1))+' %' for i in data.visits]
palette = list(sns.color_palette(palette='Paired', n_colors=len(list_country)).as_hex())
color_language=dict(zip())

fig = px.treemap(data, path=[px.Constant('2022'), 'language_name'],
                 values=data.percentage,
                 color=data.language_name,
                 color_discrete_map=color_country,
                 hover_name=Label_per,
                )
fig.update_layout(margin = dict(t=50, l=25, r=25, b=25), showlegend=True)
fig.show()




# data['Y'] = 1
# data['X'] = list(range(len(data)))

# label = [i+'<br>'+str(j)+'<br>'+str(k)+'%' for i,j,k in zip(data.language_name,
#                                                             data.visits,
#                                                             data.percentage)]

# palette = list(sns.color_palette(palette='Paired', n_colors=len(list_country)).as_hex())

# fig = px.scatter(data, x='X', y='Y',
#                  color='language_name', color_discrete_sequence=palette,
#                  size='visits', text=label, size_max=90
#                 )
# fig.update_layout(width=900, height=320,
#                   margin = dict(t=50, l=0, r=0, b=0),
#                   showlegend=False
#                  )
# fig.update_traces(textposition='top center')
# fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
# fig.update_yaxes(showgrid=False, zeroline=False, visible=False)
# fig.update_layout({'plot_bgcolor': 'white',
#                    'paper_bgcolor': 'white'})
# fig.show()
