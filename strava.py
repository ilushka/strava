# to obtain authorization code (in browser):
# GET https://www.strava.com/oauth/authorize?client_id=XXXXX&redirect_uri=http://www.moskovko.com&response_type=code&approval_prompt=auto&scope=read_all,activity:read_all

# to obtain access & refresh tokens:
# POST https://www.strava.com/oauth/token?client_id=XXXXX&client_secret=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX&grant_type=authorization_code&code=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# https://www.strava.com/api/v3/activities/2047257038 -H "Authorization: Bearer 158d13baae57a0ce42f3d5d0645c466cd6fbd4a4"

import requests
import sys
import json
from datetime import datetime
import calendar

METERS_IN_MILE = 1609.34
METERS_IN_FOOT = 0.3048
SECONDS_IN_HOUR = 3600

total_miles = 0
total_elevation = 0
total_hours = 0
h = {"Authorization": "Bearer 158d13baae57a0ce42f3d5d0645c466cd6fbd4a4"}
page = 1
year = 2018

def get_totals(alist):
  d_total = 0
  ft_total = 0
  h_total = 0
  for a in alist:
    d_total += (int(a["distance"]) / METERS_IN_MILE) 
    ft_total += (int(a["total_elevation_gain"]) / METERS_IN_FOOT) 
    h_total += (int(a["moving_time"]) / SECONDS_IN_HOUR) 
  return {"distance": d_total, "elevation": ft_total, "hours": h_total}

while True:
  after = calendar.timegm(datetime(year, 1, 1).timetuple())
  before = calendar.timegm(datetime(year + 1, 1, 1).timetuple())

  while True:
    url = 'https://www.strava.com/api/v3/athlete/activities?after={}&before={}&per_page=100&page={}'.format(after, before, page)
    r = requests.get(url, headers=h)
    if r.status_code == 200:
      j = json.loads(r.text)
      if len(j) == 0:
        break
      totals = get_totals(j)
      total_miles += totals["distance"]
      total_elevation += totals["elevation"]
      total_hours += totals["hours"]
      page += 1
    else:
      break

  if total_miles > 0:
    print("{}: {} mi, {} ft, {} h".format(year, total_miles, total_elevation, total_hours))
    total_miles = 0
    total_elevation = 0
    total_hours = 0
    page = 1
    year -= 1
  else:
    break

