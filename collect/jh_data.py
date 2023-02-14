import pandas as pd

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
    
    # get dataframe from url
    df = pd.read_csv(url)

    return df

















# outputs - where to save these files?
deaths = get_jh_data("deaths")
cases = get_jh_data("cases")
vaccinations = get_jh_data("vaccinations")
tests = get_jh_data("tests")