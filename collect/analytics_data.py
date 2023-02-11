import requests
import json
import os

#!!! Set this in your enviorment or the code won't run!!!
key = os.environ['ANALYTICS_API_KEY']


def get_analytics_by_agency(agency, date_range, report_type, max_pulls=100, limit=10000):
    ''''
    Pulls JSON files filtered by agency.

    Inputs:
        agency (str): filter agency
        data_range (tup): tuple containing start and end of time frame.
        report_type: type of analytics report
        max_pull (int): optional, number of pulls made at one time
        limit (int): optional, limit to API request 
        '''

    start_date, stop_date = date_range

    
    url = f"https://api.gsa.gov/analytics/dap/v1.1/agencies/{agency}/reports/{report_type}/data?api_key={key}"
    params = {"limit" : limit, "before" : stop_date, "after" : start_date }
    pull_count = 0 
    results = []

    while pull_count < max_pulls: 
        curr_response = requests.get(url, params)
        results += curr_response.json()
        pull_count += 1
        
        if curr_response.json()[-1]['date'] == stop_date:
            
            return results
    
    







