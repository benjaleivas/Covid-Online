# Author: Jack and Claire
from .clean_analytics import TrafficData, LanguageData, TrafficSourceData
from .clean_covid_data import CovidData


# Jack and Claire
def collect_analytics_data(agency, years, report_type, sites):
    """
    Collects and cleans data on website visits, browser langague,
    and traffic source for use in visualizations; exports CSV files to the 
    data folder
    """
    # ALL VISITS - Jack
    all_visits = TrafficData(agency, years["traffic"], report_type["traffic"])

    # Fetch data from the API
    all_visits.fetch_data()

    # Divide into yearly dataframes
    all_visits.split_by_year()

    # Collect visits by week
    all_visits.sum_by("week")

    # Count visits to all sites by week
    all_visits.sum_by("week", aggregate=True)

    # Subsets weekly data by key sites to track
    all_visits.find_sites(sites)

    all_visits.export()

    # VISITS BY TRAFFIC SOURCE - Claire

    # for each of the three time periods, get traffic source data
    for time_period in years["traffic-source"]:
        visits_by_traffic_source = TrafficSourceData(
            agency, time_period, report_type["traffic-source"]
        )
        # fetch data from analytics API
        visits_by_traffic_source.fetch_data()
        # categorizes url fragment into different buckets
        visits_by_traffic_source.add_source_categories()
        # saves as CSV in data folder
        visits_by_traffic_source.export()

    # VISITS BY USER LANGUAGE - Claire
    visits_by_language = LanguageData(
        agency, years["language"], report_type["language"]
    )
    visits_by_language.fetch_data()
    visits_by_language.add_language_columns()
    visits_by_language.export()


# Claire
def collect_covid_data():
    """
    Collects, cleans, and locally saves daily COVID-19 cases and deaths.
    """
    covid = CovidData()

    # webscrapes all COVID data from NYT github site
    covid.fetch_data()

    # splits data by year
    covid.split_by_year()

    # saves each chunk of daily covid data as a csv
    covid.export()
