#!/usr/bin/env python

import csv
import urllib
import json
import time
import os
from time import strftime

workers=[]
unique_zips = []
api_key = "Ar5IGdiMiQdXWyvdFbt97lkcBfu0jiNQ91TyluFQzYFRN3WhR_VsH56_pjLxUBKg"
loopcount = 0
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
    
#######################################
# MAIN
#######################################

kenilworth_NJ = '07033'
error_zips = []


with open('commute_times.txt', 'a') as myFile:
	myFile.write("Zipcode  Duration (s)  Distance\n")
myFile.close()

start_time = strftime("%m-%d-%Y %H:%M")

#1 week from start
end_time = start_time.replace(strftime("-%d-"), str(int(strftime("%d"))+7))

while True:
	#exits after a week
	if strftime("%m-%d-%Y %H:%M") is end_time:
		exit()
		
	#Gets data every half hour and hour
	if "00" in strftime("%M") or "30" in strftime("%M"):
		loopcount += 1
		
		#print time to file
		with open('commute_times.txt', 'a') as myFile:
			myFile.write("Time: " +strftime("%m-%d-%Y %H:%M:%S") + "\n")
		myFile.close()
		
		#Print data for each zip to file	
		for zips in unique_zips:
			print zips
	
			try:
				commute = get_commute(zips, kenilworth_NJ)
				with open('commute_times.txt', 'a') as myFile:
					myFile.write(zips + "  " + str(commute[0]) + "  " + str(commute[1]) + "\n")
				myFile.close()
				time.sleep(0.1) #API has a 10 requests per second limit
			except IndexError:
				#error_zips.append(zips)
				donothing=1




