import pandas as pd
from collect.auxilary_data import get_nyt_data

def get_cleaned_covid_data(save_locally=False):
    """
    Uses collect and clean functions to get cleaned COVID data.

    Inputs: save locally (bool)
      Defaults to False. If True, saves to "data" folder
    Returns: Cleaned Dataframe of COVID data.
    """
    nyt_data = get_nyt_data()

    nyt_data_new_cols = add_columns_for_daily_cols(nyt_data)
    final_nyt_data = convert_date_col(nyt_data_new_cols)

    if save_locally:
        filepath = "data/cleaned_covid_data.csv"
        final_nyt_data.to_csv(filepath)

    return final_nyt_data

def add_columns_for_daily_cols(covid_df):
    """
    Takes pandas Dataframe with cumulative totals, and creates two new columns,
    "daily_cases" and "daily_deaths".

    Inputs: NYT COVID pandas dataframe, output from get_nyt_data().

    Returns: NYT COVID dataframe with two additional columns.
    """
    #raise an AssertionError if both columns are not in the input df
    assert 'cases' in covid_df, "Column 'cases' not in dataframe input."
    assert 'deaths' in covid_df, "Column 'deaths' not in dataframe input."
    
    covid_df['daily_cases'] = covid_df['cases'].diff()
    covid_df['daily_deaths'] = covid_df['deaths'].diff()

    # hardcode the first observation to have the right values, not NAN
    covid_df.loc[0, 'daily_cases'] = 1
    covid_df.loc[0, 'daily_deaths'] = 0

    return covid_df

def convert_date_col(covid_df):
    """
    Takes pandas Dataframe with a date column, and returns a column of dates
    into datetime objects.
    """
    covid_df['date'] = pd.to_datetime(covid_df['date'])

    return covid_df
