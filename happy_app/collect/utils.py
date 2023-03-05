##########################
### CONSTANT VARIABLES ###
##########################

# See below for all the data we hard coded into our data pipeline.

## constants used in analysis/

KEY_DATES_2020 = {
    "2020-03-13": "COVID-19 Declared National Emergency",
    "2020-05-08": "FDA Authorizes First COVID-19 Test",
    "2020-12-11": "FDA Authorizes Pfizer Vaccine",
}

KEY_DATES_2021 = {
    "2021-03-08": "CDC Approves Safe Gathering for Vaccinated Individuals",
    "2021-07-27": "CDC Recommends Masks Due to Delta Variant",
    "2021-11-19": "Omnicron Surge Begins; CDC Urges Booster Shots",
}

KEY_DATES_2022 = {"2022-01-24": "Omnicron accounts for 99\% of COVID-19 Cases"}

KEY_DATES = {
    "2020-03-13": "COVID-19 Declared National Emergency",
    "2020-05-08": "FDA Authorizes First COVID-19 Test",
    "2020-12-11": "FDA Authorizes Pfizer Vaccine",
    "2021-03-08": "CDC Approves Safe Gathering for Vaccinated Individuals",
    "2021-07-27": "CDC Recommends Masks Due to Delta Variant",
    "2021-11-19": "Omicron Surge Begins; CDC Urges Booster Shots",
    "2022-01-19": "Due to Omicron surge, Biden launches online platform to order free COVID-19 tests"
}

## constants used in clean/

# dictionary of strings to look for using regular expressions
COMMON_SOURCES = {
    #social media sources
    "Facebook": ["facebook", "^Facebook$", "education.fb.com"],
    "Twitter" : ["twitter", "^t.co$"],
    "Instagram" : ["instagram"],
    "Snapchat" : ["snapchat"],
    "Reddit" : ["reddit"],
    "TikTok": ["tiktok"],
    "YouTube": ["youtube"],
    "Spotify": ["spotify"],
    # search engines
    "Google" : ["google"] ,
    "DuckDuckGo" : ["duckduckgo"],
    "Bing" : ["bing"],
    "Yahoo": ["yahoo"],
    "Baidu": ["baidu"],
    # gov sources
    "Other .gov": [".gov$", "lnks.gd", "govdelivery", "gquery", ".us$"],
    # direct site
    "Direct Link": ["(direct)"],
    # other interesting sites
    "Wikipedia": ["wikipedia"],
    "Other .org": [".org$"],
    "Other .edu": [".edu$"],
    "Other .com": [".com$"],
    "Oracle": ["eloqua"],
}

SOURCE_TYPES = {
    "Social Media": ["Facebook", "Twitter", "Instagram", "Snapchat","Reddit","TikTok","YouTube", "Spotify"],
    "Search Engine": ["Google", "DuckDuckGo","Bing","Yahoo","Baidu"],
    "Direct Link": ["Direct Link"],
    ".gov Sites": ["Other .gov"],
    "Other": ["Wikipedia", "Other .org", "Other .edu", "Other .com", "Oracle"]
}


## NOT USED YET - MAYBE DELETE COMPLETELY

## constants used in collect/

AGENCY_NAME = {
    "HHS": "health-human-services",
    "AID": "agency-international-development",
    "AG": "agriculture",
    "COM": "commerce",
    "DOD": "defense",
    "EDU": "education",
    "EN": "energy",
    "EPA": "environmental-protection-agency",
    "EO": "executive-office-president",
    "GSA": "general-services-administration",
    "HHS": "health-human-services",
    "HS": "homeland-security",
    "HUD": "housing-urban-development",
    "DOI": "interior",
    "DOJ": "justice",
    "DOL": "labor",
    "NASA": "national-aeronautics-space-administration",
    "NARA": "national-archives-records-administration",
    "NSF": "national-science-foundation",
    "NRC": "nuclear-regulatory-commission",
    "OPM": "office-personnel-management",
    "USPS": "postal-service",
    "SBA": "small-business-administration",
    "SSA": "social-security-administration",
    "STATE": "state",
    "DOT": "transportation",
    "TRES": "treasury",
    "VA": "veterans-affairs",
}

REPORT_NAME = {
    "DOWNLOAD": "download",
    "TRAFFIC": "traffic-source",
    "DEVICE": "device-model",
    "DOMAIN": "domain",
    "SITE": "site",
    "DOMAIN-2": "second-level-domain",
    "LANG": "language",
    "BROWSER_OS": "os-browser",
    "BROWSER_WINDOWS": "windows-browser",
    "BROWSER": "browser",
    "WINDOWS_IE": "windows-ie",
    "OS": "os",
    "WINDOWS": "windows",
    "IE": "ie",
    "DEVICE": "device",
}

