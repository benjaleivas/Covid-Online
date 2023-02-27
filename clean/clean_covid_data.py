import pandas as pd
from .datatype import DataType
from collect.auxilary_data import get_covid_data
from collections import defaultdict
import itertools


class CovidData(DataType):
    def __init__(self):
        # initializing variables that will be modidied when data is fetched
        self.data = defaultdict(None)
        self.years = None
        self.time_period = "daily"
    
    def fetch_data(self):
        """
        Uses collect and clean functions to get cleaned COVID data.

        Returns: None. Sets self.data as cleaned Dataframe of COVID data.
        """
        # use helper function to scrape COVID data from NYT github
        print(f"Collecting daily COVID data.")
        covid_data = get_covid_data()

        # use helper functions to clean data
        print(f"Cleaning daily COVID data.")
        covid_data = add_columns_for_daily_cols(covid_data)
        covid_data = convert_date_col(covid_data)

        # remove all data from 2023 to standardize across other data inputs
        covid_data = covid_data[covid_data.date.dt.year != 2023]

        # save data and years as instance attributes
        self.data['covid_data'] = covid_data
        self.years = self.data['covid_data']['date'].dt.year.unique()

    
    def split_by_year(self, in_place=True):
        """
        Splits aggegrated yearly data into one dataframe per year.
        """
        by_year = defaultdict(None)
        for year in self.years:
            year_df = self.data['covid_data'][self.data['covid_data'].date.dt.year == int(year)]
            # Convert date back to string to merge datasets
            by_year[year] = year_df

        if in_place:
            self.data = by_year
        else:
            #save as separate attribute if in_place=False
            self.modified_data = by_year


    def sum_by(self, time_period="daily", in_place=True):
        """
        """
        self.time_period = time_period
        valid_time_periods = ["daily", "weekly", "monthly"]
        
        #raise an AssertionError if time_period is not "daily", "weekly", "monthly"
        assert time_period in valid_time_periods, "Time period must be 'daily', 'weekly', or 'monthly'."
        
        for year, df in self.data.items():
            if time_period == "daily":
                # don't do anything if aggregator should be day, already at day level
                return
            elif time_period == "weekly":
                # create new column by week
                df['week'] = df.date.dt.isocalendar().week
                by_time_period = df.groupby('week').sum()
            elif time_period == "monthly":
                # create new column by month
                df['month'] = df.date.dt.month
                by_time_period = df.groupby('month').sum()

            if in_place:
                self.data[year] = by_time_period
            else:
                #save as separate attribute if in_place=False
                self.modified_data[year] = by_time_period
        

    def export(self, modified=False):

        export_data = self.data
        if modified:
            export_data = self.modified_data

        for (year, df) in export_data.items():
            df.to_csv(f"data/{year}_{self.time_period}_covid_data.csv", index=False)


## HELPER FUNCTIONS TO CLEAN COVID DATA

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
