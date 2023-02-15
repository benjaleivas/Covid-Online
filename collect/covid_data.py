import pandas as pd
from sodapy import Socrata
import json
import requests
from .utils import cdc_report_name

def get_jh_data(data_type):
    """
    Retrieves COVID-19 data from the Center for Systems Science and 
      Engineering (CSSE) at John Hopkins University by data_type

    Inputs: 
      data_type (str): either "cases", "deaths", "vaccinations", or "tests"

    Returns: pandas Dataframe with all cases or deaths by county
    """
    data_types = ["cases", "deaths", "vaccinations", "tests"]
    
    assert data_type in data_types, "data_type input not valid. Must be 'cases', 'deaths', 'vaccinations', or 'tests'."
    
    # CASES AND DEATHS
    if data_type in ["cases", "deaths"]:
        # use "cases" as input to function, but "confirmed" is in url string
        if data_type == "cases":
            data_type = "confirmed"

        url = f"https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_{data_type}_US.csv"

    # VACINATIONS AND TESTS
    if data_type in ["vaccinations", "tests"]:
        if data_type == "vaccinations":
            url_string = "testing_data/county_time_series_covid19_US"
        else:
            #if data_type == tests
            url_string = "vaccine_data/us_data/time_series/time_series_covid19_vaccine_us"
        
        url = f"https://github.com/govex/COVID-19/raw/master/data_tables/{url_string}.csv"    
    
    # get dataframe from url - but can turn this into a dict if needed
    df = pd.read_csv(url)

    return df

#TODO: might need to separate CDC data grab into multiple functions bc the 
   # API filters for vacctinaions and cases and deaths are different
   # or alternatively standardize them a bit better in the call

def get_cdc_data(report_type, start_date, end_date):
    """

    Inputs:
      report_type (str) - options are "vaccinations" or "cases and deaths"
      start_date (str), expects YYYY-MM-DD
      end_date (str), expects YYYY-MM-DD
    
    Returns: 

    """
    # needed for accessing cdc data (don't need API token for public data)
    client = Socrata("data.cdc.gov", None)
    
    results = client.get(
        cdc_report_name[report_type],
        where= f"start_date={start_date}"
        #where= f"end_date={end_date}"
    )

    # Convert to pandas DataFrame
    #results_df = pd.DataFrame.from_records(results)
    
    return results


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

# jh_deaths = get_jh_data("deaths")
# jh_cases = get_jh_data("cases")
# jh_vaccinations = get_jh_data("vaccinations")
# jh_tests = get_jh_data("tests")
# unemployment = get_bls_data("2020", "2022")