import pandas as pd
import numpy as np
import os

def save_csv(last_campaign, ward, name):
    last_campaign = last_campaign.reset_index(drop=True)
    if not os.path.isdir("json"):
        os.mkdir("json")
    last_campaign.to_json(os.path.join(
                            "json",
                            "{} - {}.json".format(ward, name)), orient='index')