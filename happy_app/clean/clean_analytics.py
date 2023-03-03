import pandas as pd
import itertools
from collect.analytics_data import get_analytics_by_agency, get_analytics_by_report
from collect.utils import REPORT_NAME, AGENCY_NAME
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

# clean traffic source data


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
