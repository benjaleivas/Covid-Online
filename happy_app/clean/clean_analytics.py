
# Author: Jack (Class structure) and Claire (implementation for report types)

import pandas as pd
import itertools
from happy_app.collect.analytics_data import get_analytics_by_agency, get_analytics_by_report
from happy_app.collect.auxiliary_data import get_language_codes, get_census_language_data
from happy_app.collect.utils import REPORT_NAME, AGENCY_NAME
from happy_app.clean.create_source_categories import add_source_labels
from .datatype import DataType
from collections import defaultdict
import re
import warnings

# Turn off pandas warnings
warnings.simplefilter("ignore")

# Jack
class AnalyticsData(DataType):
    '''
    Parent class for all Analytics.gov data. 
    '''
    def __init__(self, report_type, years):
        self.report_type = report_type
        self.years = years
        self.data = defaultdict(None)
        self.raw_data = defaultdict(None)
        self.to_export = []

    def sum_by(self, time_range, aggregate=False, export=True):
        '''
        Cleans dataframe and sums values across inputed time range. If aggregate
        is true, variables are collapsed into one summed observation per time
        range. If not, variables are summed by report_type (e.g by site)
        '''
        if time_range == "week":
            self.count_weeks()

        to_sum = defaultdict(None)
        for name, report in self.data.items():
            # Set group by column name via regex 
            col = re.sub(r"\d{4}_", "", name)
            # Alternative way to set col name depending on inputed report type
            if "domain" in name:
                col = "domain"
            if aggregate:
                to_sum[f"{name}_by_{time_range}_total"] = report.groupby(
                    ["year", time_range], as_index=False).sum()
            else:
                to_sum[f"{name}_by_{time_range}"] = report.groupby(
                    [col, time_range, "year"], as_index=False).sum()

        if export:
            self.to_export.append(to_sum)
        else:
            return to_sum

    def split_by_year(self):
        '''
        Splits aggegrated yearly data into multiple dataframes per year.
        '''
        by_year = defaultdict(None)
        for pair in itertools.product(self.report_type, self.years):
            report, year = pair
            # Convert date to datetime
            self.data[report].date = pd.to_datetime(self.data[report].date)
            # Selects only observations that match the correct year
            year_df = self.data[report][self.data[report].date.dt.isocalendar().year == int(year)]

            by_year[f"{year}_{report}"] = year_df
        
        # Sets data in yearly format
        self.data = by_year

    def export(self):
        '''
        Exports data as CSV files in the data folder.
        '''

        for export_dct in self.to_export:
            for name, df in export_dct.items():
                # Remove daily date if not removed already
                if "date" in df.columns:
                    df.drop("date", axis=1, inplace=True)
                print(f"Saving {name}.")
                df.to_csv(f"happy_app/data/{name}.csv", index=False)

    def count_weeks(self):
        '''
        Adds column to track weeks for a given. Used when aggregating data 
        by week 
        '''
        for report in self.data:
            self.data[report]["week"] = self.data[report]["date"].dt.isocalendar().week
            self.data[report]["year"] = self.data[report]["date"].dt.isocalendar().year

    def undo_changes(self):
        '''
        Reverts data into format received from Analytics.gov
        '''
        self.data = self.raw_data

    def fetch_data(self):
        '''
        Fetches data from API for specified reports.
        '''
        for report in self.report_type:
            print(f"Collecting data on {report}.")
            self.raw_data[report] = get_analytics_by_agency(self.agency, 
                                        (self.years[0], self.years[-1]), report)
       
        self.data = self.raw_data

# Jack
class TrafficData(AnalyticsData):
    '''
    Child class specific to traffic data. Used to clean data to visualize
    overall visit trends to HHS websites
    '''
    def __init__(self, agency, years, report_type):
        super().__init__(report_type, years)
        self.agency = agency

    def find_sites(self, sites, export=True):
        """
        Subsets data by specified sites
        """
        by_site = defaultdict(None)
        for name, data in self.data.items():
            # pass data if aggregated
            if "total" in name:
                pass
            by_site[f"{name}_key_sites"] = data[data["domain"].isin(sites)]

        if export:
            self.to_export.append(by_site)
        else:
            return by_site


# Claire
class TrafficSourceData(AnalyticsData):
    def __init__(self, agency, years, report_type=["traffic-source"]):
        super().__init__(agency, years)
        self.agency = agency
        self.report_type = report_type
        self.start_date, self.end_date = years

    def add_source_categories(self, export=True):
        """
        Takes a dataframe of TrafficSourceData, and adds two columns: "source cat"
        and "source type" which offer two levels of categorization of the source
        data for better analysis. 
        """

        Inputs (DataFrame): a dataframe that is a value of the self.data atrribute
            of the TrafficSourceData class
        Returns (DataFrame): the same dataframe with two added columns, "source cat"
            (str) and "source type" (str).
        """
        with_source_categories = {}

        # fills initialized dict with new dataframes with two new columns
        for key, df in self.data.items():
            with_source_categories[key] = add_source_labels(df)

        if export:
            self.to_export.append(with_source_categories)
        else:
            # if export is false, method will return the new data
            return with_source_categories

    def export(self):
        """
        Slight change from inherited class to include the start and end dates
        in the file name because it is not split by year.
        """

        for export_dct in self.to_export:
            for name, df in export_dct.items():
                print(f"Saving {name}.")
                df.to_csv(
                    f"happy_app/data/{self.start_date}_to_{self.end_date}_{name}.csv",
                    index=False,
                )


# Claire
class LanguageData(AnalyticsData):
    def __init__(self, agency, years, report_type="language"):
        super().__init__(agency, years)
        self.agency = agency
        self.report_type = report_type

    def add_language_columns(self, export=True):
        """
        Creates new column of cleaned language names for better categorization.
        """
        # get language codes from webscraper functions, then simplify
        language_codes = get_language_codes()

        # create copy of self.data to modify in this function
        with_language_cols = {key: val for key, val in self.data.items()}

        # for every dataframe in self.data
        for key, df in with_language_cols.items():
            if "language" in with_language_cols[key].columns:
                # simplify language codes to be just the characters before the dash
                with_language_cols[key]["language"] = with_language_cols[key][
                    "language"
                ].str.replace(r"\-(.*)", "", regex=True)
                # add new column with just the langauge name using dictionary
                with_language_cols[key]["language_name"] = (
                    with_language_cols[key]["language"].map(language_codes).str.strip()
                )

        if export:
            self.to_export.append(with_language_cols)
        else:
            # if export is false, method will return the new data
            return with_language_cols
