import pandas as pd
from collect.analytics_data import get_analytics_by_agency, get_analytics_by_report
from collect.utils import REPORT_NAME, AGENCY_NAME
from datatype import DataType
from collections import defaultdict

# Switch to classes to keep track of agency type, report name as attributes
# and more easily toggle between summed data and site/domain level


class Agency_Data(DataType):
    def __init__(self, agency, years, report_type):
        self.agency = agency
        self.years = years
        self.report_type = report_type
        self.data = defaultdict(None)

    def fetch_data(self):
        """
        Fetches and structures API data based on years and number of reports

        Returns named tuple holding pandas df for each report type.
        """
        for report in self.report_type:
            self.data[report] = get_analytics_by_agency(self.agency, self.years, report)

    def sum_by(self, df, col, in_place=True):
        """
        Cleans dataframe and sums values
        """
        to_sum = self.data
        for report in to_sum:
            to_sum[report] = to_sum[report].drop("id", axis=1)
            to_sum[report].groupby(col, as_index=False).sum()

        if in_place:
            self.data = to_sum
        else:
            self.modified_data = to_sum


class Report_Data(DataType):
    def __init__(self, report_type, years):
        self.report_type = report_type
        self.years = years
        self.raw_pd = get_analytics_by_report(self.report_type, self.years)

    # Add fetch_data method

    def sum_by(self, col, save_locally=False):
        """
        Sums values by specified col
        """
        clean = self.raw_pd.drop("id", axis=1)

        if save_locally:
            clean.to_csv("data/cleaned_daily_analytics_data.csv")

        return clean.groupby(col, as_index=False).sum()
