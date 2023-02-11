import requests
import json
import os
from .utils import report_agency, report_name

#!!! Set this in your environment or the code won't run!!! 
# (see README.md for instructions on how to get your own API key)
key = os.environ['ANALYTICS_API_KEY']

# decompose further, breaking apart the function below into two parts

# TODO: function to get a FULL day of data

# TODO: function with date range that sends each day to previous function and aggregates


def get_analytics_by_agency(agency, date_range, report_type, max_pulls=100, limit=10000):
    ''''
    Pulls JSON files filtered by agency.

    Inputs:
        agency (str): filter agency
        data_range (tup): tuple of strs containing start and end of time frame.
            Expects YYYY-MM-DD. For example: ("2020-02-01", "2020-02-02")
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
        '''

    start_date, stop_date = date_range
    
    url = f"https://api.gsa.gov/analytics/dap/v1.1/agencies/{agency}/reports/{report_type}/data?api_key={key}"
    params = {"limit" : limit, 
              "before" : stop_date, 
              "after" : start_date }
    pull_count = 0 
    results = []

    while pull_count < max_pulls: 
        curr_response = requests.get(url, params)
        results += curr_response.json()
        pull_count += 1
        
        if curr_response.json()[-1]['date'] == stop_date:
            return results
    
    # added second return statement bc was returning none if it didnt hit the stop data conditional
    return results
