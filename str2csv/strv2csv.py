#!/usr/bin/env python
# encoding=utf8
'''
    File name: str2csv.py
    Description: export strava activity parameters to a csv file.
    Python Version: 2.7.13
'''
__author__ = "Alberto Andrés"
__license__ = "GPL"

from stravalib import Client
import sys, csv
reload(sys)
sys.setdefaultencoding('utf8')

################################################################################
#   Constants    
################################################################################
csv_filepath = "C://Users//hp//Desktop//myfile.csv"
start_date = "2016-10-31T00:00:00Z"
end_date = "2017-10-31T00:00:00Z"
m_in_km_c = 1000.0
ms2kmh_c = 3.6
ms2minkm_c = 16.666666666667

# https://www.strava.com/settings/api
MY_STRAVA_CLIENT_ID=00000
MY_STRAVA_CLIENT_SECRET='FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF'
STORED_ACCESS_TOKEN='FFFFFFFFFFFFFFFFFFFFFfFFFFFFFFFFFFFFFFFF'
################################################################################

# Begin the code

# client = Client()
# url = client.authorization_url(client_id=MY_STRAVA_CLIENT_ID,
                               # redirect_uri='http://127.0.0.1:5000/authorization')                               
# print '\n' + url + '\n'

# Get current athlete details
client = Client(access_token=STORED_ACCESS_TOKEN)
client.get_athlete() 
#print client.get_athlete()

out = csv.writer(open(csv_filepath,"w"), delimiter=';',quoting=csv.QUOTE_MINIMAL)

# List the next parameters of activities.
# https://pythonhosted.org/stravalib/api.html#stravalib.model.Activity
for activity in client.get_activities(after = start_date, before = end_date, limit=None):
    data = []
    name = '{0.name}'.format(activity)
    data.append(name)
    start_date_local = '{0.start_date_local}'.format(activity)
    data.append(start_date_local)
    type = '{0.type}'.format(activity)
    data.append(type)
    distance = '{0.distance}'.format(activity)
    distance = distance.strip('m')
    distance = format(float(distance)/m_in_km_c, '.3f')
    data.append(distance)
    total_elevation_gain = '{0.total_elevation_gain}'.format(activity)
    total_elevation_gain = total_elevation_gain.strip('m')  
    total_elevation_gain = format(float(total_elevation_gain), '.2f')
    data.append(total_elevation_gain)
    average_speed = '{0.average_speed}'.format(activity)
    average_speed = average_speed.strip('m / s')  
    if type == 'Ride':
        average_speed = format(float(average_speed)*ms2kmh_c, '.2f')
    elif type == 'Run':
        average_speed = format(ms2minkm_c/float(average_speed), '.2f')
    data.append(average_speed)
    moving_time = '{0.moving_time}'.format(activity)
    data.append(moving_time)
    elapsed_time = '{0.elapsed_time}'.format(activity)
    data.append(elapsed_time)    
    location_city = '{0.location_city}'.format(activity)
    data.append(location_city) 
    map = '{0.map}'.format(activity) 
    map = map.strip('<Map id=a')
    map = map.strip('resource_state=2>')
    map = 'https://www.strava.com/activities/' + map
    data.append(map)     
    out.writerow(data)
    
print '\n' + 'Generated file!!! ' + csv_filepath + '\n'
    