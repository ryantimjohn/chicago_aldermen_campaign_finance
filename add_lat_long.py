from geopy.geocoders import Nominatim, GoogleV3
from geopy.extra.rate_limiter import RateLimiter
import pandas as pd

geolocator = Nominatim(user_agent="alderman_donor_lookup", timeout=10)
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
geolocator2 = GoogleV3(api_key='AIzaSyDpQCqBm88QuIENEkewK3QK3UtOA2rgXbU', timeout=10)
geocode2 = RateLimiter(geolocator2.geocode, min_delay_seconds=1)

def add_lat_long(last_campaign):
    last_campaign['full_address'] = (last_campaign['address1'] + ', ' +
            last_campaign['city'] + ', ' +
            last_campaign['state'] + ' ' +
            last_campaign['zipcode'])

    total = len(last_campaign.index)
    counts = 0

    for index, row in last_campaign.iterrows():
        counts += 1
        try:
            if last_campaign.loc[index, 'lat'] == -87.66063 and last_campaign.loc[index, 'lng'] == 41.87897:
                print("Looking up row {} of {}".format(counts, total))
                location = geolocator.geocode(last_campaign.loc[index, 'full_address'])
                last_campaign.loc[index, 'lat'] = location.latitude
                last_campaign.loc[index, 'lng'] = location.longitude
        except AttributeError:
            print("This address not found: {}".format(last_campaign.loc[index, 'full_address']))
            try:
                location = geolocator2.geocode(last_campaign.loc[index, 'full_address'])
                last_campaign.loc[index, 'lat'] = location.latitude
                last_campaign.loc[index, 'lng'] = location.longitude
                print("Here are the lat and lng that Google came up with: {}, {}".format(
                    last_campaign.loc[index, 'lat'],
                    last_campaign.loc[index, 'lng']
                ))
            except AttributeError:
                print("Even Google couldn't find this address!")
                last_campaign.loc[index, 'lat'] = last_campaign.loc[index, 'lat'] + (((random.random()*2)-1)*.01)
                last_campaign.loc[index, 'lng'] = last_campaign.loc[index, 'lng'] + (((random.random()*2)-1)*.01)
        # location = geolocator.geocode(full_address)
        # try:
        #     last_campaign.loc[index, 'lat'] = location.latitude
        #     last_campaign.loc[index, 'long'] = location.longitude
        # except AttributeError as e:
        #     pass
        # if last_campaign.loc[index, 'lat']:
        #     print(last_campaign.loc[index, 'lat'])
        # else:
        #     print(full_address)
    return(last_campaign)
