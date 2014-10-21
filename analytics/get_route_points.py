#!/usr/bin/env python

#Gets commute data from the zip codes of a csv over the span of a week

import csv
import urllib
import json
import time
import os
from time import strftime

workers=[]
unique_zips = []
api_key = "Ar5IGdiMiQdXWyvdFbt97lkcBfu0jiNQ91TyluFQzYFRN3WhR_VsH56_pjLxUBKg "

#read in csv file rows into array
with open('merck.csv') as f:
    reader = csv.reader(f)
    for row in reader:
    	workers.append(row)

#get a list of unique zipcodes
for row in workers:
	if row[1] not in unique_zips:
		unique_zips.append(row[1])


#returns a list of workers in that org
def get_org(group_letter):
	x = []
	for row in workers:
		if 'Org ' + group_letter in row[2]:
			x.append(row)
	return x

#returns a list of workers with that zipcode
def get_zipcode(zipcode):
	x = []
	for row in workers:
		if zipcode in row[1]:
			x.append(row)
	return x

#returns a list of workers with that zipcode and org
def get_zipcode_and_org(zipcode, group_letter):
	x = []
	for row in workers:
		if zipcode in row[1] and 'Org ' + group_letter in row[2]:
			x.append(row)
	return x
	

# get commute distance and time in seconds
# returns a list [distance, time]	
def get_commute(start_loc, end_loc):
	URL = "http://dev.virtualearth.net/REST/V1/Routes/Driving?&wp.0="+start_loc+"&wp.1="+end_loc+"&key="+api_key
	
	bingResponse = urllib.urlopen(URL)
	data = json.loads(bingResponse.read())
	
	commute = []
	
	#get total duration and time
	try:
		commute.append(data["resourceSets"][0]["resources"][0]["travelDurationTraffic"])
	except KeyError:
		commute.append(data["resourceSets"][0]["resources"][0]["travelDuration"])
	commute.append(data["resourceSets"][0]["resources"][0]["travelDistance"])

	return commute
	
# get commute distance and time in seconds
# returns a list [distance, time]	
def get_points(start_loc, end_loc):
	URL = "http://dev.virtualearth.net/REST/V1/Routes/Driving?&wp.0="+start_loc+"&wp.1="+end_loc+"&routePathOutput=Points&key="+api_key
	
	bingResponse = urllib.urlopen(URL)
	data = json.loads(bingResponse.read())
	
	points = []
	
	#get lat/long points
	
	points.append(data["resourceSets"][0]["resources"][0]["routePath"]["line"]["coordinates"])
	
	return points
    
#######################################
# MAIN
#######################################

kenilworth_NJ = '07033'
error_zips = []

#Print points for each route to file	
for zips in unique_zips:
	print zips
	try:
		points = get_points(zips, kenilworth_NJ)
		with open('route_points.txt', 'a') as myFile:
			myFile.write("Zip:"+zips + "  " + ''.join(str(points)) + "\n")
		myFile.close()
		time.sleep(0.1) #API has a 10 requests per second limit
	except IndexError:
		#error_zips.append(zips)
		print "IndexError!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
	except KeyError:
		print "KeyError!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"


