# Generates JSON files for the website, listing the amount from small donors
# and big donors and how they change with/without FEO. Also finds three
# "undesireable" donor industries for each alderperson whose contributions shrink
# the most when FEO is applied
import pandas as pd
import os
pd.options.mode.chained_assignment = None  # turn off copy warning
#this script is kinda judgemental
BAD_PEOPLE=['financial','developer', 'candidate', 'pac', 'property_man', 'party', 'realestate'] #labels from the classifier that we want to highlight
sector_name_remap={'financial':'Financial sector','candidate':'Political candidates','property_man':'Property management companies','small donors':'Small donors (< $175)','developer':'Property developers','realestate':'Real estate companies','local individual ':'People in their ward','pac':'PACs','construction':'Construction companies','retail':'Retail businesses','unclassified local business':'Other business in their ward','nonlocal individual ':'People from outside their ward','union':'Labor unions','unclassified nonlocal business':'Other businesses outside their ward','party':'Political parties'}

def industry_before_after(donations, industry): #returns estimate of contributions from this industry before and ater FEO
    this_industry=donations.loc[donations['classified_type'] == industry, 'amount']
    industry_total=0
    industry_total_feo=0
    for index in range(0,this_industry.shape[0]):
        industry_total=industry_total+this_industry.ix[index]
        #compute FEO projection
        if this_industry.ix[index] > 500:
            temp_feo=500
        else:
            temp_feo=this_industry.ix[index]
        if this_industry.ix[index] < 175:
            feo_contrib=this_industry.ix[index] * 6
        else:
            feo_contrib=175*6
        industry_total_feo=industry_total_feo+temp_feo+feo_contrib
    return [sector_name_remap[industry],industry_total,industry_total_feo,industry_total-industry_total_feo]

        
        
    
def make_web_json(donations,ward):
    not_itemized_sum=donations.ix[donations.shape[0]-1].amount #the not-itemized total is the last row in frame
    donations=donations.drop(donations.index[donations.shape[0]-1]) #remove non itemized
    under_175_sum = not_itemized_sum+donations.loc[donations['amount'] <= 175, 'amount'].sum()
    over_500_sum = donations.loc[donations['amount'] >= 500, 'amount'].sum()
    under_175_sum_after_feo = under_175_sum * 7
    over_500_sum_after_feo = donations.loc[donations['amount'] >= 500, 'amount'].count() * (500 + (175 * 6))
    feo_effects=[]
    for group in BAD_PEOPLE:
        feo_effects.append(industry_before_after(donations,group))
    feo_effects=pd.DataFrame(feo_effects)
    feo_effects=feo_effects.sort_values(3,ascending=False)
    feo_effects=feo_effects.drop(feo_effects.index[3:len(BAD_PEOPLE)]) #Keep just the top three bad industries with the largest drop in contributions when FEO is applied
    feo_effects=feo_effects.append([["Small donors",under_175_sum,under_175_sum_after_feo,under_175_sum-under_175_sum_after_feo]])
    if not os.path.isdir("web_json"):
        os.mkdir("web_json")
    before_feo=feo_effects[[0,1]]
    before_feo['before_after']='before'
    before_feo.columns=["type","amount","before_after"]
    after_feo=feo_effects[[0,2]]
    after_feo['before_after']='after'
    after_feo.columns=["type","amount","before_after"]
    all_sector=before_feo.append(after_feo,ignore_index=True)
    all_sector.to_json(os.path.join("web_json","Ward{}_sector.json".format(ward)), orient='records')

    funding_data = [['Small donations (under $175)', under_175_sum,"before"], ['Large donations (over $500)', over_500_sum,"before"],['Small donations (under $175)', under_175_sum_after_feo,"after"], ['Large donations (over $500)', over_500_sum_after_feo,"after"]]
    df_funding_data = pd.DataFrame(funding_data, columns = ['type', 'amount','before_after'])
    df_funding_data.to_json(os.path.join( "web_json","Ward{}_totals.json".format(ward)), orient='records')
    
    
        



    
