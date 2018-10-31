import urllib.request as request
import re
import pandas as pd

def add_not_itemized(last_campaign, boe_encrypted_committee_id):
    response = request.urlopen(r"https://www.elections.il.gov/CampaignDisclosure/SumCommitteeTotalsByLatest.aspx?ddlRptPdBegDate=lEtZ72ugJfwwp00kq6cDTaVGPuvjH3FH&ddlRptPdEndDate=yZamMQxPS3i8XqKHn6lloX9Sda8gT2DH&chkSumActive=Qd%2bzqNNUDz17teiXzJ5TaA%3d%3d&ddlSumNameSearchType=Zmi%2bDERw7rnJw0XAnrzUl8xm1ic3AbiN&txtSumName=L7J3SVvlhxk%3d&ddlSumAddressSearchType=MlCtiLJ47yvHJedg8ZJInlbXtg3pvUce&txtSumAddress=L7J3SVvlhxk%3d&ddlSumCitySearchType=MlCtiLJ47yvHJedg8ZJInlbXtg3pvUce&txtSumCity=L7J3SVvlhxk%3d&ddlState=L7J3SVvlhxk%3d&txtSumZip=L7J3SVvlhxk%3d&txtSumZipThru=L7J3SVvlhxk%3d&txtCmteID="
                    + boe_encrypted_committee_id +
                    r"%3d%3d&txtCmteLocalID=L7J3SVvlhxk%3d&txtCmteStateID=L7J3SVvlhxk%3d")
    p = re.compile(r'<span id="ctl00_ContentPlaceHolder1_lblIndivContribNI" class="BaseText">\$([0-9,.]*)</span>')
    m = p.findall(response.read().decode('utf-8'))[0]
    m = m.replace(',','')
    m = int(float(m))
    not_itemized = {'last_name' : "Non-itemized donations",
                    'amount' : m,
                    'donor_type_size' : 'Donations under $175',
                    'donation_location' : 'Non-itemized donations under $150',}
    df = pd.DataFrame([not_itemized], columns=not_itemized.keys())
    last_campaign = pd.concat([last_campaign, df], axis = 0, sort=False)
    return last_campaign
