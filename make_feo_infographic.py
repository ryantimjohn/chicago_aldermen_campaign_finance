import process_il_sunshine as pis
import make_chart_from_data as mcfd
from add_lat_long import add_lat_long
from save_json import save_json
from save_csv import save_csv
from html_safe import html_safe
from alderman_info_list import alderman_info_list
from since_last_election import since_last_election
from add_not_itemized import add_not_itemized
import urllib
import pandas as pd
import re
from make_low_vs_high import make_low_vs_high

# TODO: get lat and long from chicago Cityscape, make a thing that puts only the totals into two JSONS, one before one after FEO ordinance
# TODO: investigate marker clustering Google Maps API: https://developers.google.com/maps/documentation/javascript/marker-clustering https://developers.google.com/maps/solutions/store-locator/nyc-subway-locator
<<<<<<< HEAD
# TODO: update dimple script to only use JSON totals
=======
# TODO: output all entries with exactly the same address
>>>>>>> e3a29d2ff2aba4f8d8c7b5b1dbd89af5160644a5

print("Welcome to the Chicago Fair Elections Alderman Lookup Program!\n\nPlease enter a search here with the 'End Date:' field set to the most recent date it'll do:\n\nhttps://www.elections.il.gov/CampaignDisclosure/SumCommitteeTotalsbyLatest.aspx\n\nInput this number for Committee ID:\n20808\n\nNow copy and paste the URL here (use your mouse instead of a keyboard shortcut or you'll break the program)\n\n")
url = input("Please past the URL here: ")
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
    last_campaign = pis.preprocess_data(df)
    if start_date == "lEtZ72ugJfwwp00kq6cDTaVGPuvjH3FH":
        last_campaign = since_last_election(last_campaign)
    last_campaign = pis.group_and_aggregate(last_campaign)
    make_low_vs_high(last_campaign, boe_encrypted_committee_id, start_date, end_date, ward)
    last_campaign = pis.ward_geo_lookup(last_campaign)
    last_campaign = add_lat_long(last_campaign)
    last_campaign['coord'] = tuple(zip(last_campaign['lng'],  last_campaign['lat']))
    last_campaign = pis.add_donation_location(last_campaign, ward)
    last_campaign = add_not_itemized(last_campaign, boe_encrypted_committee_id, start_date, end_date)
    save_csv(last_campaign, ward, alderman_name)
    last_campaign = html_safe(last_campaign)
    save_json(last_campaign, ward, alderman_name)



    #mcfd.make_infographic(last_campaign, ward, alderman_name)
