from alderman_url_list import alderman_url_list
import re
from pprint import pprint

print("\nWelcome to BOA extractor!\nPlease go to this URL:\n\nhttps://www.elections.il.gov/CampaignDisclosure/SumCommitteeTotalsbyLatest.aspx\n\n")


output=[]

with open("alderman_info_list.py", 'x') as f:
    for e in alderman_url_list:
        o = []
        o.append(e[0])
        o.append(e[1])
        p = re.compile(r'committee_id=(\d*)')
        m = p.findall(e[2])[0]
        o.append(m)
        print('Enter this number in the search:\n{}'.format(m))
        url = input('Please paste the URL here: ')
        p = re.compile(r'txtCmteID=([A-Za-z0-9_%]*)%3d%3d')
        m = p.findall(url)[0]
        o.append(m)
        output.append(o)

    f.write("#in the format [ward, alderman_name, committee_id, boa_encrypted_committee_id]\nalderman_info_list = ")
    pprint(output, stream=f)
