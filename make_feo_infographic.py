import process_il_sunshine as pis
import make_chart_from_data as mcfd
from add_lat_long import add_lat_long
from save_csv import save_csv
from alderman_url_list import alderman_url_list
import urllib
import pandas as pd

for alderman in alderman_url_list:
    print('Working on {} from ward {}.'.format(alderman[1], alderman[0]))
    url = alderman[2]
    ward = alderman[0]
    name = alderman[1]
    response = urllib.request.urlopen(url)
    df = pd.read_csv(response)
    last_campaign = pis.preprocess_data(df)
    last_campaign = pis.group_and_aggregate(last_campaign)
    last_campaign = pis.add_donor_type_size(last_campaign)
    #last_campaign = add_lat_long(last_campaign)
    save_csv(last_campaign, ward, name)
    #last_campaign = pis.ward_lookup(last_campaign)
    #last_campaign = pis.add_donation_location(last_campaign, ward)

    #mcfd.make_infographic(last_campaign, ward, name)
