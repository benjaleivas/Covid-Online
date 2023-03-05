from . import link

# Variables to replicate our project
agency = "health-human-services"
years = [2020, 2021]
domain_level = ["second-level-domain"]
sites = [
    "cdc.gov",
    "vaccines.gov",
    "vacunas.gov",
    "covid.cdc.gov",
    "covid.gov",
    "covidtests.gov",
]

if __name__ == "__main__":
    link.collect_analytics_data(agency, years, domain_level, sites)
