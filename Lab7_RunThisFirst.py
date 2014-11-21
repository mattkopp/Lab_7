#Matt Koppelman
#GIS501
#Lab 7

import TwitterSearch
from geopy import geocoders
from TwitterSearch import *
import geopy
import arcpy
from arcpy import env
import csv
import string
import os
 

env.workspace = r"C:\Users\Matt\Documents\UWTacoma\GIS501\GitHub\Lab_7\TwitterApp\results"
arcpy.env.overwriteOutput = True


def geo(location):
    g = geocoders.GoogleV3()
    loc = g.geocode(location)
    return loc.latitude, loc.longitude

#Dybbuugb
try:
    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    tso.set_keywords(['ebfg']) # let's define all words we would like to have a look for
    tso.set_include_entities(False) # and don't give us all those entity information	

    #object creation with secret token
    ts = TwitterSearch(
        consumer_key = 'KmjqQQkZDmlXVh7JTCsWhUT3u',
        consumer_secret = '2Y6ZTj4wfLl3FtzVnqGYOGQPl7ZYnIfH9vhbqYqqINtKSV7SVt',
        access_token = '361007642-rJRndwoXv09DZ8Olh9ooyG5Wv0dXPPy0bIW6MoQM',
        access_token_secret = 'BgSOv1PBGJfk1qjLAIFvss1IeEfuGBSvpdhXmWOnhX8fa'
     )

    CoordList = []     # this is where the fun actually starts :)
    for tweet in ts.search_tweets_iterable(tso):
		#print tweet
        if tweet['place'] is not None:
            #print( '@%s tweeted: %s' % ( tweet['user']['screen_name'], tweet['text']))
            (lat, lng) = geo(tweet['place']['full_name'])
            CoordList.append((float(lat), float(lng)))	
            print '(' + str(lat) +', ' +str(lng)+')'
	#print CoordList
	
	
	csvfile = r"C:\Users\Matt\Documents\UWTacoma\GIS501\GitHub\Lab_7\TwitterApp\results\ebfg.csv"
	csvfields = ["Originalxy"]
	with open (csvfile, 'wb') as field:
		writer = csv.DictWriter(field, csvfields, delimiter = ',')
		writer.writeheader()
	
	with open(csvfile, "a") as output:
		writer = csv.writer(output, lineterminator='\n')
		for val in CoordList:
			writer.writerow([val])
	


	


except TwitterSearchException as e: # take care of all those ugly errors if there are some
    print(e)

execfile(r"C:\Users\Matt\Documents\UWTacoma\GIS501\GitHub\Lab_7\TwitterApp\Lab7_Final_Split.py")