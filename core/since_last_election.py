import datetime as dt

def since_last_election(df):
    #selecting for the last_campaign
    last_campaign = df[(df['received_date'] >= dt.datetime(2015, 2, 24))]
    return last_campaign
