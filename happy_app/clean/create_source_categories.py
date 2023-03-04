import pandas as pd
import itertools
from happy_app.collect.analytics_data import get_analytics_by_agency, get_analytics_by_report
from happy_app.collect.auxilary_data import simplify_language_codes, get_census_language_data
from happy_app.collect.utils import REPORT_NAME, AGENCY_NAME, COMMON_SOURCES, SOURCE_TYPES
from .datatype import DataType
from collections import defaultdict
import re


def create_source_category_dict(data):
    """
    Takes a dataframe and creates a dictionary url fragments called "sources"
    in analytics data (e.g. "facebook.com") to meaningful source categories
    (e.g. "Facebook").

    Inputs (DataFrame): a dataframe that is a value of the self.data atrribute
        of the TrafficSourceData class 
    Returns (dict): a dictionary mapping categorized url fragments to their 
        source category (e.g. {'facebook.com': 'Facebook'})
    """
    source_categories = {}

    # convert all url fragments in dataframe to lowercase
    all_sources = data["source"].str.lower() 
    
    for key, url_regexs in COMMON_SOURCES.items():
        # initialize value as list for each key
        source_categories[key] = set()
        
        # for every regex, get all unique url fragments that match that category
        for regex in url_regexs:
            sources_with_regex = list(all_sources[all_sources.str.contains(regex, regex=True)].unique())
            # add all instances of url sources that meet the regex to the set
            source_categories[key].update(sources_with_regex)

    # reverse dictionary so key is URL fragment and value is the cat
    source_categories_reversed = {value: k for k,values in 
                                  source_categories.items() 
                                  for value in values}
    
    return source_categories_reversed


def add_source_labels(data):
    """
    Takes a dataframe of TrafficSourceData, and adds two columns: "source cat" 
    and "source type" which offer two levels of categorization of the source
    data for analytics. 

    Inputs (DataFrame): a dataframe that is a value of the self.data atrribute
        of the TrafficSourceData class 
    Returns (DataFrame): the same dataframe with two added columns, "source cat"
    (str) and "source type" (str).
    """
    # get source categories using helper function
    source_categories = create_source_category_dict(data)

    # create a dictionary that maps each source cat to a more general source type
    source_types_reversed = {value: k for k,values in SOURCE_TYPES.items() for value in values}

    # maps the source to source categories
    data["source cat"] = data["source"].str.lower().map(source_categories, na_action='ignore')
    
    # maps the source to source types, using source categories if no source type
    data["source type"] = data["source cat"].map(source_types_reversed, na_action='ignore')
    data["source type"] = data["source cat"].where(data["source type"].isna(), data["source type"])

    return data