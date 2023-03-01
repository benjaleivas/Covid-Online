import requests
import os
import time
from pprint import pprint
import pandas as pd
import re

#!!! Set this in your environment or the code won't run!!!
# (see README.md for instructions on how to get your own API key)
key = os.environ["ANALYTICS_API_KEY"]

# decompose further, breaking apart the function below into two parts

# TODO: function to get a FULL day of data

# TODO: function with date range that sends each day to previous function and aggregates


def get_analytics_by_agency(agency, date_range, report_type, limit=10000):
    """
    Pulls JSON files filtered by agency.

    Inputs:
        agency (str): filter agency
        data_range (tup): tuple of strs containing start and end of time frame.
            Expects YYYY-MM-DD. For example: "("2020-02-01", "2020-02-02")"
        report_type: type of analytics report. Dates are inclusive
        max_pull (int): optional, number of pulls made at one time
        limit (int): optional, limit to API request

    Returns: list of dictionaries (the content of the dictionaries depends
      on the type of report selected, but may include:
            id (int)
            date (str): in format YYYY-MM-DD
            report_name (str)
            domain (str)
            visits (int)
    """
    start_year, stop_year = date_range
    # Check if time is year-to-year or day-to-day
    # if re.fullmatch(r"\d{4}-\d{2}-\d{2}", start_year):
    #     before = stop_year
    #     after = start_year
    # else:
    before = f"{stop_year}-12-31"
    after = f"{start_year}-01-01"

    results = []
    pull_count = limit
    page = 1

    while pull_count == limit:
        time.sleep(1)
        url = f"https://api.gsa.gov/analytics/dap/v1.1/agencies/{agency}/reports/{report_type}/data?api_key={key}"
        print(f"Fetching page {page} of request...")
        params = {
            "limit": limit,
            "before": before,
            "after": after,
            "page": page,
        }

        curr_response = requests.get(url, params)
        results += curr_response.json()
        page += 1

        pull_count = len(curr_response.json())

        # Edge case for when last page of results equals limit
        if (pull_count == limit) and (
            curr_response.json()[-1]["date"] == params["after"]
        ):
            break

    df = pd.json_normalize(results)
    return df.drop("id", axis=1)


def get_analytics_by_report(report, date_range, limit=10000):
    """
    Pulls JSON files filtered by report.

    Inputs:
        report (str): filter report
        data_range (tup): tuple of strs containing start and end of time frame.
            Expects YYYY-MM-DD. For example: "("2020-02-01", "2020-02-02")"
        report_type: type of analytics report
        max_pull (int): optional, number of pulls made at one time
        limit (int): optional, limit to API request

    Returns: list of dictionaries (the content of the dictionaries depends
      on the type of report selected, but may include:
            id (int)
            date (str): in format YYYY-MM-DD
            report_name (str)
            domain (str)
            visits (int)
    """
    start_year, stop_year = date_range
    # Check if time is year-to-year or day-to-day
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", start_year):
        before = stop_year
        after = start_year
    else:
        before = f"{stop_year}-12-31"
        after = f"{start_year}-01-01"
    results = []
    pull_count = limit
    page = 1

    while pull_count == limit:
        time.sleep(1)
        url = f"https://api.gsa.gov/analytics/dap/v1.1/reports/{report}/data?api_key={key}"
        print(f"Fetching page {page} of request...")
        params = {
            "limit": limit,
            "before": before,
            "after": after,
            "page": page,
        }

        curr_response = requests.get(url, params)

        results += curr_response.json()
        page += 1

        pull_count = len(curr_response.json())

        # Edge case for when last page of results equals limit
        if (pull_count == limit) and (
            curr_response.json()[-1]["date"] == params["after"]
        ):
            break

    df = pd.json_normalize(results)
    return df.drop("id", axis=1)
