from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import pandas as pd

geolocator = Nominatim(user_agent="alderman_donor_lookup")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

def add_lat_long(last_campaign):
    last_campaign['full_address'] = (last_campaign['address1'] + ', ' +
            last_campaign['city'] + ', ' +
            last_campaign['state'] + ' ' +
            last_campaign['zipcode'])
    last_campaign['coord'] = last_campaign['full_address'].apply(geocode).apply(
         lambda location: (location.latitude, location.longitude) if location else None)
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
