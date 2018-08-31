import pandas as pd
import numpy as np
import os

def save_csv(last_campaign, ward, name):
    last_campaign = last_campaign.reset_index(drop=True)
    if not os.path.isdir("csv"):
        os.mkdir("csv")
    last_campaign.to_csv(os.path.join(
                            "csv",
                            "{} - {}.csv".format(ward, name)), sep = '\t')
