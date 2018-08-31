import html
import pandas as pd

def html_safe(last_campaign):
    last_campaign = last_campaign.applymap(lambda x: html.escape(x, quote=True) if type(x) is str else x)
    return(last_campaign)
