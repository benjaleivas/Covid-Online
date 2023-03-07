import pandas as pd

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