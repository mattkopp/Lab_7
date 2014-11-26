#Name: Matt Koppelman
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
 

env.workspace = r"C:\Users\Matt\Documents\UWTacoma\GIS501\GitHub\FinalProject\Results"
arcpy.env.overwriteOutput = True

try:
	def geo(location):
		g = geocoders.GoogleV3()
		loc = g.geocode(location)
		return loc.latitude, loc.longitude

except GeocoderQuotaExceeded as q:
	print(q)		
		
		

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
            #print '(' + str(lat) +', ' +str(lng)+')'
	print CoordList
	

	
except TwitterSearchException as e: # take care of all those ugly errors if there are some
    print(e)
except GeocoderQuotaExceeded as q:
	print(q)
except GeocoderTimedOut as g:
	print(g)
#execfile(r"C:\Users\Matt\Documents\UWTacoma\GIS501\GitHub\Lab_7\TwitterApp\Lab7_Final_Split.py")


proj = 4326
sr = arcpy.SpatialReference(proj)	
	
arcpy.CreateFeatureclass_management(r"C:\Users\Matt\Documents\UWTacoma\GIS501\GitHub\FinalProject\Results", "ebfg", "POINT","","","", "")
fc = (r"C:\Users\Matt\Documents\UWTacoma\GIS501\GitHub\FinalProject\Results\ebfg.shp")	
	
	
cursor = arcpy.da.InsertCursor(fc, ["SHAPE@"])
p = arcpy.Point()
pointlist = []
	
for pt in CoordList:
	p.X = pt[1]
	p.Y = pt[0]
	pointlist.append(arcpy.PointGeometry(p))
		
	for coords in pointlist:
		if coords == []:
			continue
		else:
			arcpy.CopyFeatures_management(pointlist, fc)
			arcpy.DefineProjection_management(fc, sr)
arcpy.AddXY_management(fc)
