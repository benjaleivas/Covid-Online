from . import link

# Variables to replicate our project
agency = "health-human-services"
years = {
    "traffic": [2019, 2020, 2021, 2022],
    "traffic-source": [
        ("2020-03-01", "2020-04-30"),
        ("2020-12-01", "2021-01-31"),
        ("2021-12-01", "2022-01-31"),
    ],
    "language": [2019, 2020, 2021, 2022],
}

# can we just hard code these into link?
report_type = {
    "traffic": ["domain"],
    "traffic-source": ["traffic-source"],
    "language": ["language"],
}

sites = [
    "cdc.gov",
    "vaccines.gov",
    "vacunas.gov",
    "covid.cdc.gov",
    "covid.gov",
    "covidtests.gov",
]

if __name__ == "__main__":
    link.collect_analytics_data(agency, years, report_type, sites)
    link.collect_covid_data()
