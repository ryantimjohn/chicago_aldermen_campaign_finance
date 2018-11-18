from geopy.geocoders import Nominatim
import process_il_sunshine as pis
import pandas as pd
import plotly.plotly as py

geolocator = Nominatim(user_agent="alderman_donor_lookup")

df = pd.read_csv('data/1.csv')
last_campaign = pis.preprocess_data(df)
last_campaign = pis.group_and_aggregate(last_campaign)
last_campaign = pis.add_donor_type_size(last_campaign)

last_campaign['location'] = last_campaign['address1'] + ' ' + last_campaign['city'] + ' ' + last_campaign['state'] + ' ' + last_campaign['zipcode']
def trygeo(x):
    try:
        return geolocator.geocode(x)
    except:
        pass

last_campaign['geocode'] = last_campaign["location"].apply(trygeo)

def trylong(x):
	try:
		return x.longitude
	except Exception as e:
		return None

def trylat(x):
	try:
		return x.latitude
	except Exception as e:
		return None


last_campaign['longitude'] = last_campaign['geocode'].apply(trylong)
last_campaign['latitude'] = last_campaign['geocode'].apply(trylat)

#starting the plot

data = [dict(
    type = 'scattergeo',
	locationmode = 'USA-states',
	lon = last_campaign['longitude'],
	lat = last_campaign['latitude'],
	text = last_campaign['last_name'],
	mode = 'markers'
	)]

layout = dict(
	title = 'Campaign Donors',
    geo = dict(
           scope='usa',
           projection=dict( type='albers usa' ),
           showland = True,
           landcolor = "rgb(250, 250, 250)",
           subunitcolor = "rgb(217, 217, 217)",
           countrycolor = "rgb(217, 217, 217)",
           countrywidth = 0.5,
           subunitwidth = 0.5
       )
)

fig = dict(data=data, layout=layout)
py.plot(fig, validate=False, filename='CampaignFinancestuff')


last_campaign.to_csv('test_df.csv')
