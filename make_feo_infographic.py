import process_il_sunshine as pis
import make_chart_from_data as mcfd
import pandas as pd
import os

alderman_list = pis.alderman_list

# TODO: Get off using the numbered CSVs and download everything off Illinois Sunshine

for ward, alderman in enumerate(alderman_list, 1):
    print('Working on {} from ward {}.'.format(alderman, ward))
    df = pd.read_csv(os.path.join('data', r'{}.csv'.format(ward)))
    last_campaign = pis.preprocess_data(df)

    last_campaign = pis.group_and_aggregate(last_campaign)
    last_campaign = pis.add_donor_type_size(last_campaign)
    #last_campaign = pis.ward_lookup(last_campaign)
    last_campaign = pis.add_donation_location(last_campaign, ward)

    mcfd.make_infographic(last_campaign, ward, alderman)
