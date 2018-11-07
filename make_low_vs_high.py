import pandas as pd
import urllib.request as request
import re
import os

def make_low_vs_high(last_campaign, boe_encrypted_committee_id, start_date, end_date, ward):
    #get not_itemized donations
    response = request.urlopen(r"https://www.elections.il.gov/CampaignDisclosure/SumCommitteeTotalsByLatest.aspx?ddlRptPdBegDate="
                    + start_date +
                    "&ddlRptPdEndDate="
                    + end_date +
                    "&chkSumActive=Qd%2bzqNNUDz17teiXzJ5TaA%3d%3d&ddlSumNameSearchType=Zmi%2bDERw7rnJw0XAnrzUl8xm1ic3AbiN&txtSumName=L7J3SVvlhxk%3d&ddlSumAddressSearchType=MlCtiLJ47yvHJedg8ZJInlbXtg3pvUce&txtSumAddress=L7J3SVvlhxk%3d&ddlSumCitySearchType=MlCtiLJ47yvHJedg8ZJInlbXtg3pvUce&txtSumCity=L7J3SVvlhxk%3d&ddlState=L7J3SVvlhxk%3d&txtSumZip=L7J3SVvlhxk%3d&txtSumZipThru=L7J3SVvlhxk%3d&txtCmteID="
                    + boe_encrypted_committee_id +
                    r"%3d%3d&txtCmteLocalID=L7J3SVvlhxk%3d&txtCmteStateID=L7J3SVvlhxk%3d")
    p = re.compile(r'<span id="ctl00_ContentPlaceHolder1_lblIndivContribNI" class="BaseText">\$([0-9,.]*)</span>')
    not_itemized = p.findall(response.read().decode('utf-8'))[0]
    not_itemized = not_itemized.replace(',','')
    not_itemized = int(float(not_itemized))

    under_175_sum = last_campaign.loc[last_campaign['amount'] <= 175, 'amount'].sum()
    under_175_sum += not_itemized
    over_500_sum = last_campaign.loc[last_campaign['amount'] >= 500, 'amount'].sum()
    under_175_sum_after_feo = under_175_sum * 7
    over_500_sum_after_feo = last_campaign.loc[last_campaign['amount'] >= 500, 'amount'].count() * (500 + (175 * 6))
    data = [['under_175', under_175_sum, 'before'], ['over_500', over_500_sum, 'before'],['under_175', under_175_sum_after_feo, 'after'], ['over_500', over_500_sum_after_feo, 'after']]
    df = pd.DataFrame(data, columns = ['type', 'amount', 'before_after'])
    if not os.path.isdir("json_low_high"):
        os.mkdir("json_low_high")
    df.to_json(os.path.join(
                    "json_low_high",
                    "Ward{}_before_after.json".format(ward)), orient='records')
