import re
# import donation_classifier as dc
import urllib

import pandas as pd

import utilities
from alderman_info_list import alderman_info_list
from web_json import make_web_json

# TODO: output all entries with exactly the same address

print("Welcome to the Chicago Fair Elections Alderman Lookup Program!\n\nPlease enter a search here with the 'End Date:' field set to the most recent date it'll do:\n\nhttps://www.elections.il.gov/CampaignDisclosure/SumCommitteeTotalsbyLatest.aspx\n\nInput this number for Committee ID:\n20808\n\nNow copy and paste the URL here (use your mouse instead of a keyboard shortcut or you'll break the program)\n\n")
url = input("Please paste the URL here: ")
p = re.compile(r'RptPdEndDate=([A-Za-z0-9_%]*)&')
end_date = p.findall(url)[0]

start_date = input("Thanks! Enter 'y' if you want to get info just since the last election or 'n' if you want to do it for all time.")
if start_date == 'y':
    start_date = "lEtZ72ugJfwwp00kq6cDTaVGPuvjH3FH"
else:
    start_date = "Vaz6rTDHIxMrCObtEAAPgq%2fxFmcLN2ZQ"

for alderman in alderman_info_list:
    print('Working on {} from ward {}.'.format(alderman[1], alderman[0]))
    ward = alderman[0]
    alderman_name = alderman[1]
    committee_id = alderman[2]
    boe_encrypted_committee_id = alderman[3]

    response = urllib.request.urlopen(r"https://illinoissunshine.org/api/receipts/?committee_id="+committee_id+r"&datatype=csv")
    df = pd.read_csv(response)
    df = utilities.preprocess_data(df)
    if start_date == "lEtZ72ugJfwwp00kq6cDTaVGPuvjH3FH":
        df = utilities.since_last_election(df)
    df = utilities.group_and_aggregate(df)
    df = utilities.add_donor_type_size(df)
    df = utilities.ward_geo_lookup(df)
    df = utilities.add_lat_long(df)
    df['coord'] = tuple(zip(df['lat'],  df['lng']))
    df = utilities.add_donation_location(df, ward)
    df = utilities.add_not_itemized(df, boe_encrypted_committee_id, start_date, end_date)
    # dc.add_class(df)
    # make_web_json(df,alderman[0])
    utilities.save_tsv(df, ward)
    df = utilities.html_safe(df)
    utilities.save_json(df, ward, alderman_name)
