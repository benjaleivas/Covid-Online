import warnings
import pandas as pd

# Turn off pandas warnings
warnings.simplefilter("ignore")

# Jack 
def get_yearly_percentage(years, site):
    '''
    Calculates percentage of total visits for a specified site over the 
    inputed years. Used to calculate percentages for dashboard insights.

    Aggregates percentages if multiple years are inputed

    Inputs
     years (int, lst): time range
     site (str): specified sites

    Returns: percentage of total visits for a site
    '''
    # Check for multiple years or one
    if type(years) == list:
        data = []
        for year in years:
            data.append(pd.read_csv(f"happy_app/data/{year}_domain_by_week.csv"))
        
        total = pd.concat(data, axis=0)
    else:
        total = pd.read_csv(f"happy_app/data/{years}_domain_by_week.csv")
    
    site_df = total[total["domain"] == site]

    return (site_df["visits"].sum() / total['visits'].sum()) * 100

# Benja
def get_hhs_visits_data(year):
    """
    """
    prev = pd.read_csv('happy_app/data/2019_domain_by_week_total.csv')
    post = pd.read_csv(f'happy_app/data/{year}_domain_by_week_total.csv')
    diff = post[['week']]
    diff['visits'] = post.visits - prev.visits
    return [post, prev, diff]

def get_covid_cases_data(year):
    """
    """
    data = pd.read_csv(f'happy_app/data/{year}_daily_covid_data.csv')
    data = data[['date','daily_cases']]
    data['date'] =  pd.to_datetime(data['date'])
    return data

def get_traffic_sources_data():
    """
    """
    mar_2020_apr_2020 = pd.read_csv(
        'happy_app/data/2020-03-01_to_2020-04-30_traffic-source.csv', 
        usecols=['source type', 'visits'])
    dec_2020_jan_2021 = pd.read_csv(
        'happy_app/data/2020-12-01_to_2021-01-31_traffic-source.csv', 
        usecols=['source type', 'visits'])
    dec_2021_jan_2022 = pd.read_csv(
        'happy_app/data/2021-12-01_to_2022-01-31_traffic-source.csv', 
        usecols=['source type', 'visits'])
    datasets = [dec_2021_jan_2022, dec_2020_jan_2021, mar_2020_apr_2020]

    search_engine_visits = []
    direct_link_visits = []
    gov_sites_visits = []
    social_media_visits = []
    other_sources_visits = []

    for data in datasets:
        data = data.groupby('source type', as_index=False).sum()
        search_engine_visits.append(
            data.loc[data['source type']=='Search Engine', 'visits'].values[0])
        direct_link_visits.append(
            data.loc[data['source type']=='Direct Link', 'visits'].values[0])
        gov_sites_visits.append(
            data.loc[data['source type']=='.gov Sites', 'visits'].values[0])
        social_media_visits.append(
            data.loc[data['source type']=='Social Media', 'visits'].values[0])
        other_sources_visits.append(
            data.loc[data['source type']=='Other', 'visits'].values[0])

    source_visits = [
        search_engine_visits, 
        direct_link_visits, 
        gov_sites_visits, 
        social_media_visits, 
        other_sources_visits
        ]

    return source_visits


def get_cdc_visits_data():
    """
    """
    key_sites = ['cdc.gov']
    data =  get_key_sites_data(2019, 212, key_sites)[0]
    
    return data


def get_domain_visits_data():
    """
    """
    key_sites = ['vaccines.gov', 
                'vacunas.gov', 
                'covid.cdc.gov', 
                'covid.gov', 
                'covidtests.gov']
    
    return get_key_sites_data(2020, 159, key_sites)


def get_languages_data():
    """
    """
    data = pd.read_csv("happy_app/data/language.csv", \
                        usecols=["language_name", "visits"])

    data = data.groupby("language_name", as_index=False).sum()
    data["percentage"] = round((data.visits / data["visits"].sum()) * 100, ndigits=1)
    data = data.sort_values(by="visits", ascending=False)
    data = data[data.visits > 100000000]
    data["visits"] = round(data.visits / 1000000, ndigits=1)
    data["Y"] = [1] * len(data)
    data["X"] = list(range(0, len(data)))

    return data

def get_key_sites_data(start_year, weeks_in_period, key_sites):
    """
    """
    data = pd.DataFrame(columns=['year', 'week', 'domain', 'visits'])
    for year in range(start_year,2022+1):
        all_sites = pd.read_csv(f'happy_app/data/{year}_domain_key_sites.csv')
        data = pd.concat([data, all_sites], ignore_index=True)

    idx = pd.MultiIndex.from_product(
        [data.year.unique(), data.week.unique(), data.domain.unique()], 
        names=['year', 'week', 'domain']
    )
    data = data.set_index(['year', 'week', 'domain']).reindex(idx, fill_value=0).reset_index()
    data = data.sort_values(by=['domain', 'year', 'week'], ignore_index=True)
    data['visits'] = data['visits'].astype(int)
    data['visits_cum'] = data.groupby(['domain'])['visits'].cumsum()
    data['week_count'] = data.index % weeks_in_period + 1
    data = data[data['domain'].isin(key_sites)]
    
    return (data, key_sites)
