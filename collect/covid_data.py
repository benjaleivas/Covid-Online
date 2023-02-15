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

  df = pd.read_csv(url)
  
  return df


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

    return unemployment_data


# outputs - where to save these files? a data folder locally or should we create a database?


# unemployment = get_bls_data("2020", "2022")
# cases_deaths = get_nyt_data()







## NOT SURE IF WE NEED THIS ANYMORE

# def get_jh_data(data_type):
#     """
#     Retrieves COVID-19 data from the Center for Systems Science and 
#       Engineering (CSSE) at John Hopkins University by data_type

#     Inputs: 
#       data_type (str): either "cases", "deaths", "vaccinations", or "tests"

#     Returns: pandas Dataframe with all cases or deaths by county
#     """
#     data_types = ["cases", "deaths", "vaccinations", "tests"]
    
#     assert data_type in data_types, "data_type input not valid. Must be 'cases', 'deaths', 'vaccinations', or 'tests'."
    
#     # CASES AND DEATHS
#     if data_type in ["cases", "deaths"]:
#         # use "cases" as input to function, but "confirmed" is in url string
#         if data_type == "cases":
#             data_type = "confirmed"

#         url = f"https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_{data_type}_US.csv"

#     # VACINATIONS AND TESTS
#     if data_type in ["vaccinations", "tests"]:
#         if data_type == "vaccinations":
#             url_string = "testing_data/county_time_series_covid19_US"
#         else:
#             #if data_type == tests
#             url_string = "vaccine_data/us_data/time_series/time_series_covid19_vaccine_us"
        
#         url = f"https://github.com/govex/COVID-19/raw/master/data_tables/{url_string}.csv"    
    
#     # get dataframe from url - but can turn this into a dict if needed
#     df = pd.read_csv(url)

#     return df

# jh_deaths = get_jh_data("deaths")
# jh_cases = get_jh_data("cases")
# jh_vaccinations = get_jh_data("vaccinations")
# jh_tests = get_jh_data("tests")