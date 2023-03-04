import pandas as pd
import itertools
from happy_app.collect.analytics_data import (
    get_analytics_by_agency,
    get_analytics_by_report,
)
from happy_app.collect.auxilary_data import simplify_language_codes
from happy_app.collect.utils import REPORT_NAME, AGENCY_NAME
from .datatype import DataType
from collections import defaultdict
import re

# Regex to clean URLS
# Add merge column with strings of dates and merge
# no second-level domain

# Time Periods for Traffic
# March 2020 - April 2020
# December 2020 - January 2021
# December 2021 - January 2022

# Sites to track
# cdc.gov
# covid.cdc.gov
# vacunas.cdc
# vaccines.gov
# covid.gov
# covidtests.gov


class AnalyticsData(DataType):
    def __init__(self, report_type, years):
        self.report_type = report_type
        self.years = years
        self.data = defaultdict(None)
        self.raw_data = defaultdict(None)
        self.to_export = []

    def sum_by(self, time_range, aggregate=False, export=True):
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

        if export:
            self.to_export.append(to_sum)

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

    def export(self):
        """
        Exports data to CSV files in the data folder.
        """

        for export_dct in self.to_export:
            for name, df in export_dct.items():
                df.to_csv(f"happy_app/data/update_data/{name}.csv", index=False)

    def count_weeks(self):
        """
        Adds column to track weeks for a given
        """
        for report in self.data:
            self.data[report]["week"] = self.data[report]["date"].dt.isocalendar().week
            self.data["year"] = self.data[report]["date"].dt.isocalendar().week

    def undo_changes(self):
        """
        Reverts data into format received from Analytics.gov
        """
        self.data = self.raw_data


class TrafficData(AnalyticsData):
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

    def find_sites(self, sites, export=True):
        """
        Subsets data by specified sites
        """
        by_site = defaultdict(None)
        for name, data in self.data.items():
            # pass data if aggregated
            if "total" in name:
                pass
            by_site[name] = data[data["domain"].isin(sites)]

        if export:
            self.to_export.append(by_site)


# Add SourceData class here


class LanguageData(AnalyticsData):
    def __init__(self, agency, years, report_type="language"):
        super().__init__(agency, years)
        self.agency = agency
        self.report_type = [report_type]

    def fetch_data(self):
        """
        Fetches data for specified reports.
        """
        for report in self.report_type:
            print(f"Collecting data on {report}.")
            self.raw_data[report] = get_analytics_by_agency(
                self.agency, (self.years[0], self.years[-1]), report
            )

        self.data = self.raw_data

    def clean_language_column(self):
        """
        Creates new column of language names using dictionary from
        """
        language_codes = simplify_language_codes()

        for _, df in self.data.items():
            if "language" in df.columns:
                # simplify language codes to be just the characters before the dash

                # error code: ValueError: pattern contains no capture groups
                df["language"] = df["language"].str.extract(r"^.*?(?=-)")
