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

        with_language_cols = {key: val for key, val in self.data.items()}

        # add language names for clarity
        for key, df in self.data.items():
            if "language" in df.columns:
                # simplify language codes to be just the characters before the dash
                with_language_cols[key]["language"] = df["language"].str.replace(r'\-(.*)', "", regex=True)
                # add new column with just the langauge name using dictionary
                with_language_cols[key]["language_name"] = df["language"].map(language_codes)

                # really bad match rate
                with_language_cols[key] = with_language_cols[key].merge(census_language_data, on='language_name', how='left')

                #need to re-sum by date?
                
        
        # note we have about a ~98% match rate with a language based on the codes
        self.data = with_language_cols
        