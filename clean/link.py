import pandas as pd
from collect.analytics_data import get_analytics_by_agency
from clean.clean_analytics import clean_and_sum
from collect.utils import REPORT_NAME, AGENCY_NAME

#load data for test run
covid = pd.read_csv("data/cleaned_covid_data.csv")
#make sure your api key is set for this function to run
fetch_analytics = get_analytics_by_agency(AGENCY_NAME['HHS'], 
                                            ('2021-01-01', '2021-12-31'),
                                            REPORT_NAME['SITE'])

analytics_test_data = clean_and_sum(fetch_analytics)


def merge_data(analytics_data, aux_data, save_locally=False):
    '''
    Merge cleaned Analytics.gov dataset with COVID-19 dataset

    - Work out how this should be automated.
    '''
    merged_data = pd.merge(analytics_data, aux_data, on="date", how="inner")
    merged_data.date = pd.to_datetime(merged_data.date, yearfirst=True)

    if save_locally:
        merged_data.to_csv("data/merged_test_dataset.csv")

    return merged_data