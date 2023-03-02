import pandas as pd
import json
import requests
import lxml.html
import re
import os

def get_covid_data():
    """
    Retrieves COVID-19 data from NYTimes Github, which includes date,
        total cases and total deaths.

    Inputs: None

    Returns: pandas Dataframe with three columns: date, total cases, 
        and total deaths.
    """
    url = f"https://github.com/nytimes/covid-19-data/raw/master/us.csv"
    print(f"Fetching daily COVID data.")

    covid_df = pd.read_csv(url)
    
    return covid_df


def get_language_codes():
    """
    This function restructures a webpage of langauge code data into a dictionary 
    with the keys as the language codes, and the language text as values.

    Inputs: None
    Returns: langs (dict), with the langauge code as the key (str) and the full 
    language identifier as the value (str).
    """
    url = "https://www.biswajeetsamal.com/blog/web-browser-language-identification-codes/"
    
    # get root HTML object or webpage
    html = requests.get(url).text
    root = lxml.html.fromstring(html)

    # initialize a dictionary and set row number (or future dictionary key) to 0
    langs = {}

    # collect all table rows (trs) on the webpage,
    all_rows = root.cssselect('div.entry-content table tbody')[0]

    # iterate through each row of data to see where/how to save the data to each row's dictionary
    for i, row in enumerate(all_rows):
        #unpack all table data points (tds) in the row
        text, code = row.getchildren()

        text = text.text_content()
        code = code.text_content()

        # ignore the table header
        if i == 0:
            continue
        
        langs[code] = text

    return langs

def simplify_language_codes():
    """
    Takes dict from get_language_codes() and returns a simplified version for
    identifying the 
    """
    language_codes = get_language_codes()
    simplified_languages = {}

    for key, value in language_codes.items():

        pattern_key = r'^.*?(?=-)'
        pattern_value = r'^[^\(]+'

        key_match = re.search(pattern_key, key)
        value_match = re.search(pattern_value, value)

        if key_match:
            key = key_match.group(0)

        if value_match:
            value = value_match.group(0)

        simplified_languages[key] = value
        
    return simplified_languages

def get_census_language_data():
    """
    Collects language data from 2013 Census - which is the last time this question
    was asked and collected in full detail.
    """
    # set variables for census data table
    year = "2013" # most recent year of data even though its pretty outdated
    report = "language"
    columns = "LANLABEL,EST"
    geography = "us:01"
    variable = "LAN"

    # sign up for API key here https://api.census.gov/data/key_signup.html
    # save it as local variable, os.environ["CENSUS_API_KEY"]
    API_key = os.environ["CENSUS_API_KEY"]
    
    url = f"https://api.census.gov/data/{year}/{report}?get={columns}&for={geography}&{variable}&key={API_key}"

    response = requests.get(url)
    languages_spoken = pd.DataFrame(response.json())

    # set column headers as column names
    languages_spoken.columns = languages_spoken.iloc[0]

    # remove first row of data which were column names, and unnecessary columns
    languages_spoken = languages_spoken.tail(-1)
    languages_spoken = languages_spoken.drop(columns=["us", "LAN"])
    
    return languages_spoken
    
    

###### OTHER DATA THAT WE DIDN'T END UP USING IN OUR OUTPUT

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

