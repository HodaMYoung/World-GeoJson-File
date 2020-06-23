"""The purpose of this code is to show how to create a GeoJson file from a shapefile(.shp) as
well as brief introduction to shapefiles.The .shp file used here was downloaded from Natural
Earth website. The website offers three different scale type data, i.e. small, medium and large scale.
Here, the medium size scale data was used. 

Source:

https://www.naturalearthdata.com """

#Importing necessary libraries:

import shapefile #to read and manipulate shapefiles
import pandas as pd #to manipulate DataFrames
from json import dumps #to write geojason file

#shapefile basics
"""There are different methods to read a shape file including:
1- Using Reader attribute, i.e. .Reader
   It should be noted that shapefile format contains three different files,i.e. .dfb, .shp and .shp, and
   the Reader is able to read all three shapefile components.
2- Opening the shapefile as file-like object with open, i.e. open(path,'rb')

The .shp file contains points that reresent physical locatios of verticies and arcs of geometry. While, the .dfb
file consists of records, i.e. attributes of each point in the .shp file.The shapes and records can be
read either separately with .shapes() and .records(),or simultaneously with .shapeRecords().
attribute.

The geomtry consists of different parts, where each part is collection of a series of points. Some of the main
features and attributes stored in a .shp files are:

1- bbox: A list of four elements which represent coordination of two diogonal corners, i.e.upper right and lower left,
of a box surrounding all points in the record.
2- parts: A list where each element represents the first index point of each part. It should be noted that geomtry
consists  of multiple parts which are formed by collection of points.
3- ShapeType: A numeric value represents the number of side of geometrical elements.For instance, 3 indicate that the
geomtry of parts consists of triangular elements.
4- ShapeTypeName: A string represnts the name of geometrical elements.

The field names of a shapefile are accessable when the shapefile is read. A field is a list where each element of
the list contains:
1- field names: A string represent the name of the field
2- field type: A string represnts the type of the field 
3- field length:An integer represnts the length of the field
4- decimal length: an integer represnts the number of decimal places found in “Number” fields

For instance, the  77th element of fields for the .shp file uesd here ['NAME_EN','C',44,0].Where, 'NAME_EN'
indicates the Name of countries/territories in English. 'C',44 and 0 denote the type of the field is character
with maximum length of 44 characters and 0 decimal length.

The following snippet demonstrates how to extract gemotries and their corresponding records from a .shp file as
the first stage to create a GeoJson file.""""

#Reading shapefile
sf=shapefile.Reader('worldcountries.shp')# reading the .shp file
fields=sf.fields[1:]#getting the fields and escping the first field, i.e. deletion flag
field_names = [field[0] for field in fields]#getting the name of the fields, i.e. the first element of each field
ndx=field_names.index('ADMIN')#locating the field name "Admin".It represents the international version countries' names
buffer=[]#An empty array to store the records and geomtry
for sr in sf.shapeRecords():
       atr = {field_names[ndx]:sr.record[ndx]} 
       geom = sr.shape.__geo_interface__
       buffer.append(dict(type="Feature",properties=atr, geometry=geom))
       """ It should be noted, the attributes can be customized by only including certain countries
           or modifying the names.For instance,the following lines changing the country name eSwatini to
           Eswatini
           if sr.record[ndx]=='eSwatini':
              sr.record[ndx]='Eswatini'"""
       

#writing the GeoJson file
geojson = open("CountriesAdmin.json", "w")#opening the GeoJson file named CountriesAdmin.json to assign the extracted data
geojson.write(dumps({"type": "FeatureCollection", "features": buffer}) + "\n")#writing
geojson.close()#closing the GeoJson file.

"""Recommended Website:
https://pypi.org/project/pyshp/1.1.7/"""
