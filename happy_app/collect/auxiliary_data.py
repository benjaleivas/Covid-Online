#Author: Claire

import pandas as pd
import requests
import lxml.html
import re


def get_covid_data():
    """
    Retrieves COVID-19 data from NYTimes Github, which includes the date,
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
    with the keys as the language codes, and the language text as values. This 
    is needed to categorize language codes from analytics.usa.gov data.

    Inputs: None
    Returns: langs (dict), with the langauge code as the key (str) and the full 
    language identifier as the value (str).
    """
    url = "https://www.biswajeetsamal.com/blog/web-browser-language-identification-codes/"
    
    # get root HTML object
    html = requests.get(url).text
    root = lxml.html.fromstring(html)

    # initialize a dictionary
    langs = {}

    # collect all table rows (trs) on the webpage the correspond to the table needed
    all_rows = root.cssselect('div.entry-content table tbody')[0]

    # iterate through each row of data to save the data to each row's dictionary
    for i, row in enumerate(all_rows):
        # unpack all table data points (tds) in the row
        name, code = row.getchildren()

        #extract text content
        name = name.text_content()
        code = code.text_content()

        # ignore the table header
        if i == 0:
            continue
        
        # set code as key, and name as value
        langs[code] = name

    return simplify_language_codes(langs)

def simplify_language_codes(language_codes):
    """
    Takes dict from get_language_codes() and returns a simplified version for
    identifying the main languages (e.g. simplifying "en-ca": "English (Canada)" 
    and "en-za": "English (South Africa)" all under one category "en": "English").

    Inputs: language_codes (dict)
    Returns: dictionary of simplified browser language codes, where the key 
        is the simplified browser code and the value is the name of the 
        language (e.g. "en": "English")
    """
    simplified_languages = {}

    for code, name in language_codes.items():

        #match everything before a "-" in a string
        pattern_code = r'^(.*?)(?=-)'
        #match everything after a "(" in a string
        pattern_name = r'^[^\(]+'

        code_match = re.search(pattern_code, code)
        name_match = re.search(pattern_name, name)

        if code_match:
            code = code_match.group(0)

        if name_match:
            name = name_match.group(0)

        # remove white space if needed
        simplified_languages[code] = name.strip()
        
    return simplified_languages


# FUNCTIONS FOR COLLECTING/CLEANING DATA THAT WE DIDN'T END UP USING IN OUR OUTPUT

# def get_bls_data(start_year, end_year):
#     """
#     Gets US national monthly unemployment rate from the start year to the end 
#         year (inclusive).

#     Inputs:
#         start year (str), expects YYYY
#         end year (str), expects YYYY
    
#     Returns: list of dictionaries with keys year, period (month numeric), 
#         periodName (month name), value (str), and footnotes.
#     """
#     headers = {'Content-type': 'application/json'}
#     data = json.dumps({"seriesid": ["LNS14000000"],"startyear":start_year, "endyear":end_year})
#     p = requests.post('https://api.bls.gov/publicAPI/v1/timeseries/data/', data=data, headers=headers)
#     json_data = json.loads(p.text)
    
#     unemployment_data = json_data['Results']['series'][0]["data"]
#     unemployment_df = pd.DataFrame.from_dict(unemployment_data)

#     return unemployment_df


# def get_census_language_data():
#     """
#     Collects language data from 2013 Census - which is the last time this question
#     was asked and collected in full detail.
#     """
#     # set variables for census data table
#     year = "2013" # most recent year of data even though its pretty outdated
#     report = "language"
#     columns = "LANLABEL,EST"
#     geography = "us:01"
#     variable = "LAN"

#     # sign up for API key here https://api.census.gov/data/key_signup.html
#     # save it as local variable, os.environ["CENSUS_API_KEY"]
#     API_key = os.environ["CENSUS_API_KEY"]
    
#     url = f"https://api.census.gov/data/{year}/{report}?get={columns}&for={geography}&{variable}&key={API_key}"

#     response = requests.get(url)
#     languages_spoken = pd.DataFrame(response.json())

#     # remove first row of data which were column names, and unnecessary columns
#     languages_spoken = languages_spoken.tail(-1)
#     languages_spoken = languages_spoken.drop(columns=[2, 3])

#     # set column headers as column names
#     languages_spoken.columns = ["language_name", "estimate"]
    
#     return languages_spoken
    

# def get_cleaned_bls_data(start_year, end_year, save_locally=False):
#     """
#     Uses collect and clean functions to get cleaned BLS data.

#     Inputs: save locally (bool)
#       Defaults to False. If True, saves to "data" folder
    
#     Returns: Cleaned Dataframe of BLS data.
#     """
#     bls_data = get_bls_data(start_year, end_year)
#     bls_data = convert_date_col(bls_data)

#     # rename value col and delete unnecessary columns
#     bls_data = bls_data.rename(columns = {"value": "unemployment_rate"})
#     final_bls_data = bls_data.drop(columns=['footnotes','period','year','periodName', 'month'],
#                         axis=1)

#     if save_locally:
#         filepath = "data/cleaned_bls_data.csv"
#         final_bls_data.to_csv(filepath)

#     return final_bls_data


# def convert_date_col(bls_df):
#     """
#     Takes BLS Dataframe with a year and month column, and returns a 
#     column 'date' of datetime objects, defaulting to the first of every month.
#     """
#     bls_df['month'] = bls_df['period'].str.replace("M", "")
    
#     bls_df['date'] = pd.to_datetime({"year": bls_df['year'], 
#                                      "month": bls_df['month'],
#                                      "day": 1},
#                                     yearfirst=True)

#     return bls_df
