import numpy as np
import pandas as pd
from plotly_calplot import calplot  # pip install plotly-calplot

#Load COVID data
data = pd.read_csv('data/cleaned_covid_data.csv', usecols=[1,2,3,4,5])

#Transform data
data['date'] = pd.to_datetime(data['date'])
#data = data[data['date'].dt.year == 2022]                       #filter year
#data['daily_cases_diff'] = data.daily_cases.diff().fillna(0)   #differences
#data = data[['date', 'daily_cases']]                           #relevant vars

#Plot heatmap
fig = calplot(
         data,
         x="date",
         y="daily_cases",
         years_title=True,
         showscale=True,
         colorscale='reds'
)
fig.show()
