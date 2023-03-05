# Author: Claire

import pandas as pd

def find_social_referral_frequency(start_date, end_date, source_cat):
    """
    Calculates the frequency of visits that were social referrals for a given
    traffic source. Examples of traffic sources with social referrals are:
    Facebook, Instagram, Twitter, Other .com, and Other .org.

    Inputs:
        filepath (str)
        source cat (str): must be the same exact str as source categories used
    
    Returns (float): frequency of visits that were social referrals for that source
    """
    filepath = f"happy_app/data/update_data/{start_date}_to_{end_date}_traffic-source.csv"
    
    traffic_source_data = pd.read_csv(filepath)
    
    # subset to only data within the source category provided
    traffic_source_data = traffic_source_data[traffic_source_data["source cat"] == source_cat]

    # find total number of visits from that source
    total = traffic_source_data["visits"].sum()

    # find number of visits that were social referrals from that source
    social_referrals = traffic_source_data[traffic_source_data["has_social_referral"] == "Yes"].sum()["visits"]

    # return the frequency of visits that were social referrals for that source
    return float(round(social_referrals/total*100, ndigits=0))
