import datetime as dt
import html
import json
import os
import random
import re
import urllib.request as request

import numpy as np
import pandas as pd
import requests
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import GoogleV3, Nominatim

geolocator = Nominatim(user_agent="alderman_donor_lookup", timeout=10)
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
geolocator2 = GoogleV3(api_key='AIzaSyDpQCqBm88QuIENEkewK3QK3UtOA2rgXbU', timeout=10)
geocode2 = RateLimiter(geolocator2.geocode, min_delay_seconds=1)

try:
        from api_key import api_key
except Exception: #fallback if the user doesn't have an API key
        print("Warning no Cityscape API key was found, location lookups will not work")
        api_key=None

def preprocess_data(df):
    #loading the data frame and converting received_date to datetime
    df['received_date'] = pd.to_datetime(df['received_date'])
    #replacing nan with empty string
    df = df.fillna('')
    #selecting for relevant columns, converting to correct datatypes
    df = df[['last_name','first_name','received_date','amount','occupation','employer','address1','address2','city','state','zipcode']]
    df[['last_name','first_name', 'occupation','employer','address1','address2','city','state','zipcode']] = df[['last_name','first_name', 'occupation','employer','address1','address2','city','state','zipcode']].astype(str)
    df['amount'] = df['amount'].astype(int)
    df = df.applymap(lambda x: x.strip() if type(x) is str else x)
    return df

def since_last_election(df):
    #selecting for the df
    df = df[(df['received_date'] >= dt.datetime(2015, 2, 24))]
    return df

def group_and_aggregate(df):
    #grouping by then aggregating
    dict = {'last_name':'max','first_name':'max','received_date':'max','amount':'sum','occupation':'max','employer':'max','address1':'max','address2':'max','city':'max','state':'max','zipcode':'max'}
    grouped = df.groupby(['last_name','first_name','zipcode'])
    df = grouped.agg(dict)
    return df

def add_donor_type_size(df):
    #creating a donor_type column, filling all individuals
    df['donor_type'] = pd.Series('' * len(df['received_date']), index = df.index)
    df['donor_type'] = np.where((df['first_name'] != '') , 'Individual', '')
    #assigning Political Group and business
    political_words = ["PAC", "Friends", "Union", "Committee", "Orgn", " for ", "Local", "Citizen", "Elect", "Political", "LU", "Ward", "Democratic", "Organization"]
    for word in political_words:
        df.loc[df['last_name'].str.contains(word), 'donor_type'] = 'Political Group'
    df['donor_type'] = df['donor_type'].replace('', 'Business')

    #creating and assigning <= 500 >500
    df['donation_size'] = pd.Series('' * len(df['received_date']), index = df.index)
    df.loc[df['amount'] > 500.0, 'donation_size'] = 'over $500'
    df.loc[df['amount'] < 176.0, 'donation_size'] = 'under $175'
    df['donation_size'] = df['donation_size'].replace('','between $175 and $500')
    df['donor_type_size'] = pd.Series('' * len(df['received_date']), index = df.index)
    df.loc[df['donation_size'] == 'under 175', 'donor_type_size'] = 'Donations under $175'
    df['donor_type_size'] = df['donor_type_size'].replace('', df['donor_type'] + ' ' + df['donation_size'])
    return df

def ward_geo_lookup(df):
    #ward stuff
    df['ward_if_chicago'] = ''
    df['lat'] = -87.66063
    df['lng'] = 41.87897

    total = len(df.index)
    counts = 0
    df.reset_index(drop=True, inplace=True)
    for index, row in df.iterrows():
        counts += 1
        if df.loc[index, 'city'].strip().lower() == "chicago":
            print("Looking up row {} of {}".format(counts, total))
            response = requests.get(r"https://www.chicagocityscape.com/api/index.php?address={}&city=Chicago&state=IL&key={}".format(row[6], api_key))
            result = json.loads(response.text)
            try:
                for entry in result["properties"]["boundaries"]:
                    if entry['type'] == 'ward':
                        ward = entry['slug'].split('-')[1]
                        print("Ward: {}".format(ward))
                        df.loc[index, 'ward_if_chicago'] = str(ward)
                        break
            except (TypeError, KeyError, AssertionError) as e:
                print("Error, here are the results: {}".format(result["properties"]["boundaries"]))
            try:
                df.loc[index, 'lat'] = result["geometry"]["coordinates"][0]
                df.loc[index, 'lng'] = result["geometry"]["coordinates"][1]
                if df.loc[index, 'lat'] == -87.66063 and df.loc[index, 'lng'] == 41.87897:
                    df.loc[index, 'ward_if_chicago'] = ''
            except KeyError as e:
                pass
    return df

def add_lat_long(df):
    df['full_address'] = (df['address1'] + ', ' +
            df['city'] + ', ' +
            df['state'] + ' ' +
            df['zipcode'])

    total = len(df.index)
    counts = 0

    for index, row in df.iterrows():
        counts += 1
        #if the coord is default, look up in Nominatim
        try:
            if df.loc[index, 'lat'] == -87.66063 and df.loc[index, 'lng'] == 41.87897:
                print("Looking up row {} of {}".format(counts, total))
                location = geolocator.geocode(df.loc[index, 'full_address'])
                df.loc[index, 'lat'] = location.latitude
                df.loc[index, 'lng'] = location.longitude
        except AttributeError:
            print("This address not found: {}".format(df.loc[index, 'full_address']))

            #if Openmaps doesn't have it, look up in GoogleV3
            try:
                location = geolocator2.geocode(df.loc[index, 'full_address'])
                df.loc[index, 'lat'] = location.latitude
                df.loc[index, 'lng'] = location.longitude
                print("Here are the lat and lng that Google came up with: {}, {}".format(
                    df.loc[index, 'lat'],
                    df.loc[index, 'lng']
                ))
            except AttributeError:
                print("Even Google couldn't find this address!")
                df.loc[index, 'lat'] = df.loc[index, 'lat'] + (((random.random()*2)-1)*.01)
                df.loc[index, 'lng'] = df.loc[index, 'lng'] + (((random.random()*2)-1)*.01)

    return(df)

def add_donation_location(df, ward):
    #location of the donation
    df['donation_location'] = pd.Series('' * len(df['received_date']), index = df.index)

    for index, row in df.iterrows():
        if row[13] == ward:
            df.loc[index, 'donation_location'] = 'within_ward'
        elif row[8] == "Chicago":
            df.loc[index, 'donation_location'] = 'in_Chicago_outside_ward'
        elif row[9] == "IL":
            df.loc[index, 'donation_location'] =  'in_IL_outside_Chicago'
        else:
            df.loc[index, 'donation_location'] = 'outside_IL'

    df.index = pd.RangeIndex(len(df.index))
    return df

def add_not_itemized(df, boe_encrypted_committee_id, start_date, end_date):
    response = request.urlopen(r"https://www.elections.il.gov/CampaignDisclosure/SumCommitteeTotalsByLatest.aspx?ddlRptPdBegDate="
                    + start_date +
                    "&ddlRptPdEndDate="
                    + end_date +
                    "&chkSumActive=Qd%2bzqNNUDz17teiXzJ5TaA%3d%3d&ddlSumNameSearchType=Zmi%2bDERw7rnJw0XAnrzUl8xm1ic3AbiN&txtSumName=L7J3SVvlhxk%3d&ddlSumAddressSearchType=MlCtiLJ47yvHJedg8ZJInlbXtg3pvUce&txtSumAddress=L7J3SVvlhxk%3d&ddlSumCitySearchType=MlCtiLJ47yvHJedg8ZJInlbXtg3pvUce&txtSumCity=L7J3SVvlhxk%3d&ddlState=L7J3SVvlhxk%3d&txtSumZip=L7J3SVvlhxk%3d&txtSumZipThru=L7J3SVvlhxk%3d&txtCmteID="
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
    not_itemized_df = pd.DataFrame([not_itemized], columns=not_itemized.keys())
    df = pd.concat([df, not_itemized_df], axis = 0, sort=False)
    return df

def save_csv(df, ward, name):
    df = df.reset_index(drop=True)
    if not os.path.isdir("tsv"):
        os.mkdir("tsv")
    df.to_csv(os.path.join(
                            "tsv",
                            "{} - {}.tsv".format(ward, name)), sep = '\t',
                            index=False)

def html_safe(df):
    df = df.applymap(lambda x: html.escape(x, quote=True) if type(x) is str else x)
    return(df)

def save_json(df, ward, name):
    df = df.reset_index(drop=True)
    if not os.path.isdir("json"):
        os.mkdir("json")
    df.to_json(os.path.join(
                            "json",
                            "Ward{}.json".format(ward)), orient='index')
