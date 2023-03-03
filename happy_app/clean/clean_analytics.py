import pandas as pd
import itertools
from happy_app.collect.analytics_data import get_analytics_by_agency, get_analytics_by_report
from happy_app.collect.auxilary_data import simplify_language_codes, get_census_language_data
from happy_app.collect.utils import REPORT_NAME, AGENCY_NAME
from .datatype import DataType
from collections import defaultdict
import re

# Regex to clean URLS
# Add merge column with strings of dates and merge


class AnalyticsData(DataType):
    def __init__(self, report_type, years):
        self.report_type = report_type
        self.years = years
        self.data = defaultdict(None)
        self.raw_data = defaultdict(None)

    def sum_by(self, time_range, aggregate=False):
        """
        Cleans dataframe and sums values
        """
        if time_range == "week":
            self.count_weeks()

        to_sum = defaultdict(None)
        for name, report in self.data.items():
            col = re.sub(r"\d{4}_", "", name)
            if "domain" in name:
                col = "domain"
            if aggregate:
                to_sum[f"{name}_by_{time_range}_total"] = report.groupby(
                    time_range, as_index=False
                ).sum()
            else:
                to_sum[f"{name}_by_{time_range}"] = report.groupby(
                    [col, time_range], as_index=False
                ).sum()

        self.data = to_sum

    def split_by_year(self):
        """
        Splits aggegrated yearly data into multiple dataframes per year.
        """
        by_year = defaultdict(None)
        for pair in itertools.product(self.report_type, self.years):
            report, year = pair
            # Convert date to datetime
            self.data[report].date = pd.to_datetime(self.data[report].date)
            year_df = self.data[report][
                self.data[report].date.dt.isocalendar().year == year
            ]

            by_year[f"{year}_{report}"] = year_df

        self.data = by_year

    def export(self, **reports):
        """
        Exports data to CSV files in the data folder.
        """
        to_export = self.report_type

        for (
            name,
            df,
        ) in self.data.items():
            if reports and name in reports.values():
                df.to_csv(f"data/update_data/{name}.csv", index=False)
            if not reports:
                df.to_csv(f"data/update_data/{name}.csv", index=False)

    def count_weeks(self):
        """
        Adds column to track weeks for a given
        """
        for report in self.data:
            self.data[report]["week"] = self.data[report]["date"].dt.isocalendar().week

    def undo_changes(self):
        """
        Reverts data into format received from Analytics.gov
        """
        self.data = self.raw_data


class AgencyData(AnalyticsData):
    def __init__(self, agency, years, report_type):
        super().__init__(report_type, years)
        self.agency = agency

    def fetch_data(self):
        """
        Fetches and structures API data based on years and number of reports
        """
        for report in self.report_type:
            print(f"Collecting data on {report}.")

            self.raw_data[report] = get_analytics_by_agency(
                self.agency, (self.years[0], self.years[-1]), report
            )

        self.data = self.raw_data


class ReportData(AnalyticsData):
    def __init__(self, report_type, years):
        super().__init__(report_type, years)

    def fetch_data(self):
        """
        Fetches data for specified reports.
        """
        for report in self.report_type:
            print(f"Collecting data on {report}.")
            self.raw_data[report] = get_analytics_by_report(
                report, (self.years[0], self.years[-1])
            )

        self.data = self.raw_data

    def add_language_columns(self):
        """
        Creates new column of language names using dictionary from aux data.
        Creates new columns of total langauge speakers from 2013 Census.
        """
        language_codes = simplify_language_codes()
        census_language_data = get_census_language_data()

        # add langauge names for clarity
        for _, df in self.data.items():
            if "language" in df.columns:
                # remove quotations if present
                # df["language"] = df["language"].str.replace(r"\"", "")
                
                # simplify language codes to be just the characters before the dash
                df["language"] = df["language"].str.replace(r'(?=-)', r'^(.*?)(?=-)')

                # add new column with just the langauge name using dictionary
                df["language_name"] = df["language"].map(language_codes)

                # # add census data matched on langauge name
                # df.merge(census_language_data, on='language_name', how='left')
        
        # TODO: note we have about a ~72% match rate with a language based
            # on the codes

        # TODO: when i try to revert back to raw_data the language and language
            # name columns are NaN instead of the raw version
            # assuming it is a deep copy issue
            
        
        


