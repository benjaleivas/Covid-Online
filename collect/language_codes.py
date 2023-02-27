# packages for reading in the html
import lxml.html
import requests

# packages for string manipulation and converting into a dataframe
import regex as re
import pandas as pd

def page_to_dict():
    """
    This function restructures a page of langauge code data into a dictionary 
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
    print(all_rows)

     # iterate through each row of data to see where/how to save the data to each row's dictionary
    for i, row in enumerate(all_rows):
        #unpack all table data points (tds) in the row
        text, code = row.getchildren()

        text = text.text_content()
        code = code.text_content()

        if i == 0:
            # ignore the table header
            continue
        
        langs[code] = text

    return langs