import re
from alderman_url_list import alderman_url_list

idre = re.compile(pattern='id\=(.*?)\&')

committeeids = []

for ward, name, url in alderman_url_list:
    id = re.search(idre, url).group(1)
    committeeids.append([ward, name, "https://illinoissunshine.org/committees/{}/".format(id)])

print(committeeids)
with open("committee_url_list1.py", "w") as f:
    f.write(str(committeeids))


