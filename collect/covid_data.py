import pandas as pd
import json
import requests

def get_nyt_data():
  """
  Retrieves COVID-19 data from NYTimes Github, which includes date,
    total cases and total deaths.

  Inputs: None

  Returns: pandas Dataframe with three columns: date, total cases, 
    and total deaths.
  """
  url = f"https://github.com/nytimes/covid-19-data/raw/master/us.csv"

  covid_df = pd.read_csv(url)
  
  return covid_df


def get_bls_data(start_year, end_year):
    """
    Gets US national monthly unemployment rate from the start year to the end 
      year (inclusive).

    Inputs:
      start year (str), expects YYYY
      end year (str), expects YYYY
    
    Returns: list of dictionaries with keys year, period (month numeric), 
      periodName (month name), value (str), and footnotes.
    """
    headers = {'Content-type': 'application/json'}
    data = json.dumps({"seriesid": ["LNS14000000"],"startyear":start_year, "endyear":end_year})
    p = requests.post('https://api.bls.gov/publicAPI/v1/timeseries/data/', data=data, headers=headers)
    json_data = json.loads(p.text)
    
    unemployment_data = json_data['Results']['series'][0]["data"]
    unemployment_df = pd.DataFrame.from_dict(unemployment_data)

    return unemployment_df
