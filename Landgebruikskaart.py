#library ------------------------------------------------------------------------------------------------------

import psycopg2
import shapefile
import shapefile as shp
import math
import subprocess
import random
from Shapely.geometry import Polygon
from binascii import hexlify


# Try to connect ------------------------------------------------------------------------------------------------
hostname = 'we12s300.ugent.be'
username = 'samuel'
password = 'samuvack'
database = 'fliat'
port= 5432

try:
    conn = psycopg2.connect(host=hostname, user=username, password=password, dbname=database, port=5432)
except:
    print ("I am unable to connect to the database.")

print ("Opened database successfully")

cur = conn.cursor()


'''
#----------------------------------------------------------------------------------------------------------------
#Read data

cur.execute('SELECT *  FROM "inwoners_gent" LIMIT 1')
number = cur.fetchone()

print(number)

#load shapefile --------------------------------------------------------------------------------------------------

sf = shapefile.Reader("../Gent/Gemeente_gent")

#bounding box ----------------------------------------------------------------------------------------------------

shapes = sf.shapes()
bbox = shapes[0].bbox # Retrieves the bounding box of the first shape

print (bbox) # Will print the bounding box coordinates

print ( bbox[2])

#Make grid file ---------------------------------------------------------------------------------------------------

minx,maxx,miny,maxy = bbox[0], bbox[2], bbox[1], bbox[3]
dx = 100
dy = 100

nx = int(math.ceil(abs(maxx - minx)/dx))
ny = int(math.ceil(abs(maxy - miny)/dy))

w = shp.Writer(shp.POLYGON)
w.autoBalance = 1
w.field("ID")
id=0

for i in range(ny):
    for j in range(nx):
        id+=1
        vertices = []
        parts = []
        vertices.append([min(minx+dx*j,maxx),max(maxy-dy*i,miny)])
        vertices.append([min(minx+dx*(j+1),maxx),max(maxy-dy*i,miny)])
        vertices.append([min(minx+dx*(j+1),maxx),max(maxy-dy*(i+1),miny)])
        vertices.append([min(minx+dx*j,maxx),max(maxy-dy*(i+1),miny)])
        parts.append(vertices)
        w.poly(parts)
        w.record(id)

w.save('../Gent/polygon_grid')


#Clip raster grid with Gemeente ---------------------------------------------------------------------------------------
#http://basemaptutorial.readthedocs.io/en/latest/clip.html




# The features used to clip the input features.
clipping_shp = "../Gent/Gemeente_gent.shp"
# The feature class to be created.
output_shp = "../Gent/Output.shp"
# The features to be clipped.
input_shp = "../Gent/polygon_grid.shp"

# Clipping process
subprocess.call(["ogr2ogr", "-f", "ESRI Shapefile", "-clipsrc", clipping_shp, output_shp, input_shp], shell=True)

'''
#----------------------------------------------------------------------------------------------------------------


# Insert Point data into output
cur.execute('create table if not exists output(gid serial primary key, geom geometry(Point,31370));')
# Some longitude/latitude points (in that order!)
lon_lat = [(random.random(), random.random()) for x in range(100)]
cur.executemany('insert into output(geom) values(ST_SetSRID(ST_MakePoint(%s, %s), 31370));', lon_lat)
conn.commit()

# Insert Polygon data into mypoly
cur.execute('create table if not exists mypoly(gid serial primary key, geom geometry(Polygon,31370))')
# Use Shapely to piece together exterior linear ring, and interior rings with lists of coordinates
poly = Polygon(shell=[(0,0),(0,10),(10,10),(10,0),(0,0)], holes=[[(2,2),(2,6),(7,7),(2,2)]])
poly_wkb = hexlify(poly.wkb).upper() # convert to ASCII version of WKB
cur.execute('insert into mypoly(geom) values(ST_SetSRID(%s::geometry, 31370));', (poly_wkb,))
conn.commit()



#close postgresql/postgis database ------------------------------------------------------------------------------
conn.commit()
conn.close()

