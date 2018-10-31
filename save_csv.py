import pandas as pd
import numpy as np
import os

def save_csv(last_campaign, ward, name):
    last_campaign = last_campaign.reset_index(drop=True)
    if not os.path.isdir("tsv"):
        os.mkdir("tsv")
    last_campaign.to_csv(os.path.join(
                            "tsv",
                            "{} - {}.tsv".format(ward, name)), sep = '\t',
                            index=False)
