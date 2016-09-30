import json
import googlemaps
import time

fileName = 'AtlantaDream052916.json'

gmaps = googlemaps.Client(key='API KEY HERE')
# This

with open(fileName, 'r') as f:
	# time delay helps ensure file loads correctly
	time.sleep(2)
	# counters to see which data was found with which method
	foundTwitter = 0
	foundGMaps = 0
	for line in f:
		tweet = json.loads(line)
		if tweet['coordinates'] != None:
			# if tweet has coordinate data
			print "Found with tweet data:"
			print tweet['coordinates']['coordinates']
			foundTwitter += 1
		else:
			# if there is no coordinate data, try using geocoding location endpoint using Google maps API
			if tweet['user']['location'] != '':
				# check if location field is empty, Gmaps API will throw error if input is an empty string
				geocode_result = gmaps.geocode(tweet['user']['location'])	
				if geocode_result != []:
					# if Gmaps geocode can not geocode the input, it will return a empty list	
					if 'locality' or 'sublocality' in geocode_result[0]['types']:
						# create array of lat, lng to match twitter coordinate data format
						locResult =  [geocode_result[0]['geometry']['location']['lat'] , geocode_result[0]['geometry']['location']['lng']]
						print"Found with Gmaps API:"
						print locResult
						foundGMaps +=1
print("Locations found with Twitter data only: ", foundTwitter)
print("Locations found with Google Maps API: ", foundGMaps)


