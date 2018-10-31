import process_il_sunshine as pis
import make_chart_from_data as mcfd
from add_lat_long import add_lat_long
from save_json import save_json
from save_csv import save_csv
from html_safe import html_safe
from make_kml import make_kml
from alderman_info_list import alderman_info_list
from add_not_itemized import add_not_itemized
import urllib
import pandas as pd

# TODO: make a thing that puts only the totals into two JSONS, one before one after, make a thing that requests all the urls and pulls out the non-itemized contributions, add them to the data frame, make all the donations under $175 have the same tags

make_kml()
for alderman in alderman_info_list:
    print('Working on {} from ward {}.'.format(alderman[1], alderman[0]))
    ward = alderman[0]
    alderman_name = alderman[1]
    committee_id = alderman[2]
    boe_encrypted_committee_id = alderman[3]

    response = urllib.request.urlopen(r"https://illinoissunshine.org/api/receipts/?committee_id="+committee_id+r"&datatype=csv")
    df = pd.read_csv(response)
    last_campaign = pis.preprocess_data(df)
    last_campaign = pis.group_and_aggregate(last_campaign)
    last_campaign = pis.add_donor_type_size(last_campaign)
    # last_campaign = add_lat_long(last_campaign)
    # last_campaign = pis.ward_lookup(last_campaign)
    # last_campaign = pis.add_donation_location(last_campaign, ward)
    last_campaign = add_not_itemized(last_campaign, boe_encrypted_committee_id)
    save_csv(last_campaign, ward, alderman_name)
    last_campaign = html_safe(last_campaign)
    save_json(last_campaign, ward, alderman_name)



    #mcfd.make_infographic(last_campaign, ward, alderman_name)
