# Import the Python library that supports reading CSV files
import csv
# Import the Itertools library that supports the combinations function
import itertools

# Required imports for the Google Distance/Maps Engine and API
import argparse
import httplib2
import os
import sys
import json

from apiclient import discovery
from oauth2client import file
from oauth2client import client
from oauth2client import tools
# End required Google API imports

# PART ONE: READING AND STORING THE CSV CONTENTS IN-MEMORY

# Define the list object: 'cities'
cities = []

# Open the CSV file that has the cities stored on each line
# Be sure to use the 'rU' designator for Universal Newline Mode
with open('address_list.csv', 'rU') as csvfile:
    
    # Set the parameters for the csv.reader method
    reader = csv.reader(csvfile, delimiter=',')
    
    # Recursive function to read all CSV rows
    for row in reader:
        
        row = "".join(row)
        cities.append(row)
        # Append the strings in each row to the list from above
        #cities.insert(0,row)

# Test the output of the list

# USED FOR TESTING ONLY (DELETE WHEN DCOMPLETE)
#print type(cities)
#print cities

# PART TWO: DEFINING THE COMBINATIONS AND STORING THEM AS A LIST

# Use this line of code for determining combinations
#combos = itertools.combinations(cities, 2)

# Use this line of code for determining permutations
combos = itertools.permutations(cities, 2)

usable_combos = []
for e in combos:
    usable_combos.append(e)
    
#print usable_combos

#print(len(usable_combos))

# PART THREE: REQUESTING DISTANCES FROM THE GOOGLE DISTANCE API

# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Command-line skeleton application for Google Maps Engine API.
Usage:
  $ python sample.py

You can also get help on all the command-line flags the program understands
by running:

  $ python sample.py --help

"""

# Parser for command-line arguments.
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[tools.argparser])


# CLIENT_SECRETS is name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret. You can see the Client ID
# and Client secret on the APIs page in the Cloud Console:
# <https://cloud.google.com/console#/project/176254262776/apiui>
CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')

# Set up a Flow object to be used for authentication.
# Add one or more of the following scopes. PLEASE ONLY ADD THE SCOPES YOU
# NEED. For more information on using scopes please see
# <https://developers.google.com/+/best-practices>.
FLOW = client.flow_from_clientsecrets(CLIENT_SECRETS,
  scope=[
      'https://www.googleapis.com/auth/mapsengine',
      'https://www.googleapis.com/auth/mapsengine.readonly',
    ],
    message=tools.message_if_missing(CLIENT_SECRETS))


def main(argv):
  # Parse the command-line flags.
  flags = parser.parse_args(argv[1:])

  # If the credentials don't exist or are invalid run through the native client
  # flow. The Storage object will ensure that if successful the good
  # credentials will get written back to the file.
  storage = file.Storage('sample.dat')
  credentials = storage.get()
  if credentials is None or credentials.invalid:
    credentials = tools.run_flow(FLOW, storage, flags)

  # Create an httplib2.Http object to handle our HTTP requests and authorize it
  # with our good Credentials.
  http = httplib2.Http()
  http = credentials.authorize(http)

  # Construct the service object for the interacting with the Google Maps Engine API.
  service = discovery.build('mapsengine', 'v1', http=http)

  #try:
  #  print "Success! Now add code here."
  #
  #except client.AccessTokenRefreshError:
  #  print ("The credentials have been revoked or expired, please re-run"
  #    "the application to re-authorize")

# ADD ALL ORGANIC CODE HERE:

import simplejson, urllib, pprint

print usable_combos

GEOCODE_BASE_URL = 'https://maps.googleapis.com/maps/api/directions/json'

def directions(origin, destination, sensor, key, **geo_args):
    
    geo_args.update({
        'origin': origin,
        'destination': destination  
    })
    
    url = GEOCODE_BASE_URL + '?' + urllib.urlencode(geo_args) + '&sensor=false' + '&key=' + key
    print url
    result = simplejson.load(urllib.urlopen(url))
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(result["routes"][0]["legs"][0]["distance"]["value"])
    
    #distance = result["routes"][0]["legs"][0]["distance"]["text"]
    distance = result["routes"][0]["legs"][0]["distance"]["value"]
    
    #origin = str(origin)
    #destination = str(destination)
    #distance = str(distance)
    
    # Create string variable for CSV row below
    #csv_row = str(origin + ", " + destination + ", " + distance)
    #csv_row = origin + ", " + destination + ", " + distance
    
    #print csv_row
    
    # Append to the end of an existing CSV file
    # If doesn't exist, then will create
    # df = distance file
    
    with open('distances.csv', 'a') as f:
        writer = csv.writer(f)
        #writer.writerow(csv_row)
        writer.writerow([origin, destination, distance])
        
    #df = csv.writer(open('distance_file.csv', 'a'))
    #df.write(csv_row)
    #df.close()

#directions(origin="San+Francisco", destination="New+York+City",sensor="false", key="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

for cities in usable_combos:
    start = cities[0] + " Richmond VA"
    finish = cities[1] + " Richmond VA"
    
    directions(origin=start, destination=finish,sensor="false", key="XXXXXXXXX-ENTER-YOUR-KEY-HERE-XXXXXXXXXX")
    
    print "---------------"

if __name__ == '__main__':
  main(sys.argv)
