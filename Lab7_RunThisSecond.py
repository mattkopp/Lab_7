#Matt Koppelman
#GIS501
#Lab 7


#This will run automatically from the end of the other script

import TwitterSearch
from geopy import geocoders
from TwitterSearch import *
import geopy
import arcpy
from arcpy import env
import csv
import string
import os

#removes special characters - this portion of the script sucks but it does work
csv = r"C:\Users\Matt\Documents\UWTacoma\GIS501\GitHub\Lab_7\TwitterApp\results\ebfg.csv"
OpenCSV = open(csv, 'r')
NewCSV = open(r"C:\Users\Matt\Documents\UWTacoma\GIS501\GitHub\Lab_7\TwitterApp\results\ebfg_new.csv", 'w')
for word in OpenCSV:
	NewCSV.write(word.replace('(', ''))
OpenCSV.close()
NewCSV.close()
print "done"

csv2 = r"C:\Users\Matt\Documents\UWTacoma\GIS501\GitHub\Lab_7\TwitterApp\results\ebfg_new.csv"
OpenCSV2 = open(csv2, 'r')
NewCSV2 = open(r"C:\Users\Matt\Documents\UWTacoma\GIS501\GitHub\Lab_7\TwitterApp\results\ebfg_new2.csv", 'w')
for word in OpenCSV2:
	NewCSV2.write(word.replace(',', ''))
OpenCSV2.close()
NewCSV2.close()
os.remove(csv2)
print "done"

csv3 = r"C:\Users\Matt\Documents\UWTacoma\GIS501\GitHub\Lab_7\TwitterApp\results\ebfg_new2.csv"
OpenCSV3 = open(csv3, 'r')
NewCSV3 = open(r"C:\Users\Matt\Documents\UWTacoma\GIS501\GitHub\Lab_7\TwitterApp\results\ebfg_new3.csv", 'w')
for word in OpenCSV3:
	NewCSV3.write(word.replace(')', ''))
OpenCSV3.close()
NewCSV3.close()
os.remove(csv3)
print "done"

#Creates gdb and table
csvin = r"C:\Users\Matt\Documents\UWTacoma\GIS501\GitHub\Lab_7\TwitterApp\results\ebfg_new3.csv"
arcpy.CreateFileGDB_management(r"C:\Users\Matt\Documents\UWTacoma\GIS501\GitHub\Lab_7\TwitterApp\results", "TwitterSearch")
gdb = r"C:\Users\Matt\Documents\UWTacoma\GIS501\GitHub\Lab_7\TwitterApp\results\TwitterSearch.gdb"
arcpy.TableToGeodatabase_conversion (csvin, gdb)
ebfgtbl = r"C:\Users\Matt\Documents\UWTacoma\GIS501\GitHub\Lab_7\TwitterApp\results\TwitterSearch.gdb\ebfg_new3"

env.workspace = r"C:\Users\Matt\Documents\UWTacoma\GIS501\GitHub\Lab_7\TwitterApp\results\TwitterSearch.gdb"



#splits original xy into 2 columns
arcpy.CalculateField_management(ebfgtbl, "Originalxy_x", "!Originalxy!.split(" ")[0]", "PYTHON", "")
arcpy.CalculateField_management(ebfgtbl, "Originalxy_y", "!Originalxy!.split(" ")[-1]", "PYTHON", "")


#creates point layer
outlayer = "ebfg_layer"
savedlayer = "ebfg.lyr"

arcpy.MakeXYEventLayer_management(ebfgtbl, "Originalxy_X", "Originalxy_Y", outlayer, "", "")
arcpy.SaveToLayerFile_management(outlayer, savedlayer)
arcpy.CopyFeatures_management(outlayer, r"C:\Users\Matt\Documents\UWTacoma\GIS501\GitHub\Lab_7\TwitterApp\results\TwitterSearch.gdb\ebfg_points")



#Creates a feature class that does not load files nto the correct locations in ArcMap.  When Loading the files into Google Fushion Tables it works fine.