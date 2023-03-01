import pandas as pd
import json
import requests
import lxml.html
import re

def get_covid_data():
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

def get_simplified_lang_codes():
    """
    """
    langs = get_language_codes()
    simplified_langs = {}

    for key, value in langs.items():

        pattern_key = r'^.*?(?=-)'
        pattern_value = r'^[^\(]+'

        key_match = re.search(pattern_key, key)
        value_match = re.search(pattern_value, value)

        if key_match:
            key = key_match.group(0)

        if value_match:
            value = value_match.group(0)

        simplified_langs[key] = value
        
    return simplified_langs
