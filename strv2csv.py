#!/usr/bin/env python
from stravalib import Client
# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# https://www.strava.com/settings/api
MY_STRAVA_CLIENT_ID=00000
MY_STRAVA_CLIENT_SECRET='FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF'
STORED_ACCESS_TOKEN='FFFFFFFFFFFFFFFFFFFFFfFFFFFFFFFFFFFFFFFF'

client = Client()
url = client.authorization_url(client_id=MY_STRAVA_CLIENT_ID,
                               redirect_uri='http://127.0.0.1:5000/authorization')
                               
print '\n' + url + '\n'

client = Client(access_token=STORED_ACCESS_TOKEN)
client.get_athlete() # Get current athlete details

print client.get_athlete()

print '\n'

# List of activities:
for activity in client.get_activities(after = "2016-10-31T00:00:00Z", before = "2017-10-31T00:00:00Z", limit=5):
    print("Name:{0.name} Type:{0.type} Dist:{0.distance} Time(mov):{0.moving_time}".format(activity))
    
