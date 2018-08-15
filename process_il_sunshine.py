import pandas as pd
import numpy as np
import datetime as dt
import requests
import json
try:
        from api_key import api_key
except Exception: #fallback if the user doesn't have an API key
        print("Warning no Cityscape API key was found, location lookups will not work")
        api_key=None

def preprocess_data(df):
	#loading the data frame and converting received_date to datetime
	df['received_date'] = pd.to_datetime(df['received_date'])

	#selecting for the last_campaign
	last_campaign = df[(df['received_date'] >= dt.datetime(2015, 2, 24))]

	#replacing nan with empty string
	last_campaign = last_campaign.fillna('')

	#selecting for relevant columns, converting to correct datatypes
	last_campaign = last_campaign[['last_name','first_name','received_date','amount','occupation','employer','address1','address2','city','state','zipcode']]
	last_campaign[['last_name','first_name', 'occupation','employer','address1','address2','city','state','zipcode']] = last_campaign[['last_name','first_name', 'occupation','employer','address1','address2','city','state','zipcode']].astype(str)
	last_campaign['amount'] = last_campaign['amount'].astype(int)
	return last_campaign

def group_and_aggregate(last_campaign):
	#grouping by then aggregating
	dict = {'last_name':'max','first_name':'max','received_date':'max','amount':'sum','occupation':'max','employer':'max','address1':'max','address2':'max','city':'max','state':'max','zipcode':'max'}
	grouped = last_campaign.groupby(['last_name','first_name','zipcode'])
	last_campaign = grouped.agg(dict)
	return last_campaign

def add_donor_type_size(last_campaign):
	#creating a donor_type column, filling all individuals
	last_campaign['donor_type'] = pd.Series('' * len(last_campaign['received_date']), index = last_campaign.index)
	last_campaign['donor_type'] = np.where((last_campaign['first_name'] != '') , 'Individual', '')

	#assigning Political Group and business
	political_words = ["PAC", "Friends", "Union", "Committee", "Orgn", " for ", "Local", "Citizen", "Elect", "Political", "LU", "Ward", "Democratic", "Organization"]
	for word in political_words:
		last_campaign.loc[last_campaign['last_name'].str.contains(word), 'donor_type'] = 'Political Group'
	last_campaign['donor_type'] = last_campaign['donor_type'].replace('', 'Business')

	#creating and assigning <= 500 >500
	last_campaign['donation_size'] = pd.Series('' * len(last_campaign['received_date']), index = last_campaign.index)
	last_campaign.loc[last_campaign['amount'] > 500.0, 'donation_size'] = 'over 500'
	last_campaign['donation_size'] = last_campaign['donation_size'].replace('','under 500')

	return last_campaign

def ward_lookup(last_campaign):
	#ward stuff
	last_campaign['ward_if_chicago'] = pd.Series('' * len(last_campaign['received_date']), index = last_campaign.index)

	total = len(last_campaign.index)
	counts = 0

	for index, row in last_campaign.iterrows():
		counts += 1
		if row[8].strip() == "Chicago":
			print("Looking up row {} of {}".format(counts, total))
			response = requests.get(r"https://www.chicagocityscape.com/api/index.php?address={}&city=Chicago&state=IL&key={}".format(row[6], api_key))
			result = json.loads(response.text)
			try:
				for entry in result["properties"]["boundaries"]:
					if entry['type'] == 'ward':
						ward = entry['slug'].split('-')[1]
						print("Ward: {}".format(ward))
						last_campaign.loc[index, 'ward_if_chicago'] = str(ward)
						break
			except (TypeError, KeyError, AssertionError) as e:
				print("Error, here are the results: {}".format(result["properties"]["boundaries"]))

	return last_campaign

def add_donation_location(last_campaign, ward):
	#location of the donation
	last_campaign['donation_location'] = pd.Series('' * len(last_campaign['received_date']), index = last_campaign.index)

	for index, row in last_campaign.iterrows():
		if row[13] == ward:
			last_campaign.loc[index, 'donation_location'] = 'within_ward'
		elif row[8] == "Chicago":
			last_campaign.loc[index, 'donation_location'] = 'in_Chicago_outside_ward'
		elif row[9] == "IL":
			last_campaign.loc[index, 'donation_location'] =  'in_IL_outside_Chicago'
		else:
			last_campaign.loc[index, 'donation_location'] = 'outside_IL'

	last_campaign.index = pd.RangeIndex(len(last_campaign.index))
	return last_campaign

alderman_list = ["Joe Moreno",
"Brian Hopkins",
"Pat Dowell",
"Sophia King",
"Leslie Hairston",
"Roderick Sawyer",
"Gregory Mitchell",
"Michelle Harris",
"Anthony Beale",
"Susan Sadlowski Garza",
"Patrick Thompson",
"George A. Cardenas",
"Marty Quinn",
"Ed Burke",
"Raymond Lopez",
"Toni Foulkes",
"David Moore",
"Derrick Curtis",
"Matthew O'Shea",
"Willie B. Cochran",
"Howard Brookins Jr.",
"Ricardo Munoz",
"Michael Zalewski",
"Michael Scott Jr.",
"Daniel Solis",
"Roberto Maldonado",
"Walter Burnett, Jr.",
"Jason Ervin",
"Chris Taliaferro",
"Ariel E. Reboyras",
"Milly Santiago",
"Scott Waguespack",
"Deborah Mell",
"Carrie Austin",
"Carlos Ramirez-Rosa",
"Gilbert Villegas",
"Emma Mitts",
"Nicholas Sposato",
"Margaret Laurino",
"Patrick J. O'Connor",
"Anthony Napolitano",
"Brendan Reilly",
"Michele Smith",
"Thomas M. Tunney",
"John Arena",
"James Cappleman",
"Ameya Pawar",
"Harry Osterman",
"Joseph A. Moore",
"Debra Silverstein"]
