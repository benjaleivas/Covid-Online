import pandas as pd
from collect.analytics_data import get_analytics_by_agency, get_analytics_by_report
from collect.utils import REPORT_NAME, AGENCY_NAME

#Switch to classes to keep track of agency type, report name as attributes
#and more easily toggle between summed data and site/domain level 

def clean_and_sum(analytics_df, save_locally=False):
    '''
    Cleans dataframe and sums values

    - Maybe break up into two functions
    '''
    clean = analytics_df.drop("id", axis=1)

    if save_locally:
        clean.to_csv("data/cleaned_daily_analytics_data.csv")

    return clean.groupby("date", as_index=False).sum()

