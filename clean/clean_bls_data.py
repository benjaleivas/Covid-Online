import pandas as pd
from collect.covid_data import get_bls_data

def get_cleaned_bls_data(start_year, end_year, save_locally=False):
    """
    Uses collect and clean functions to get cleaned BLS data.

    Inputs: save locally (bool)
      Defaults to False. If True, saves to "data" folder
    
    Returns: Cleaned Dataframe of BLS data.
    """
    bls_data = get_bls_data(start_year, end_year)
    bls_data = convert_date_col(bls_data)

    # rename value col and delete unnecessary columns
    bls_data = bls_data.rename(columns = {"value": "unemployment_rate"})
    final_bls_data = bls_data.drop(columns=['footnotes','period','year','periodName', 'month'],
                        axis=1)

    if save_locally:
        filepath = "data/cleaned_bls_data.csv"
        final_bls_data.to_csv(filepath)

    return final_bls_data


def convert_date_col(bls_df):
    """
    Takes BLS Dataframe with a year and month column, and returns a 
    column 'date' of datetime objects, defaulting to the first of every month.
    """
    bls_df['month'] = bls_df['period'].str.replace("M", "")
    
    bls_df['date'] = pd.to_datetime({"year": bls_df['year'], 
                                     "month": bls_df['month'],
                                     "day": 1},
                                    yearfirst=True)

    return bls_df
