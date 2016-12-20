#!/usr/bin/env python
import demjson
import requests
from bs4 import BeautifulSoup
import re
import urllib
import psycopg2
import pandas

hostname = 'we12s300.ugent.be'
username = 'samuel'
password = 'samuvack'
database = 'fliat'

# Try to connect

try:
    conn = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
except:
    print("I am unable to connect to the database.")

cur = conn.cursor()

y=1
for x in range(1, 100):
        cur.execute("UPDATE onderzoek SET aanta2 = %s where key_column = %s", (y,x))
        if (x%2)==0:
            y=y+1

y=1

for x in range(1, 100):
        cur.execute("UPDATE onderzoek SET aanta3 = %s where key_column = %s", (y,x))
        if (x%3)==0:
            y=y+1
y=1
for x in range(1, 100):
        cur.execute("UPDATE onderzoek SET aanta4 = %s where key_column = %s", (y,x))
        if (x%4)==0:
            y=y+1

y=1
for x in range(1, 100):
        cur.execute("UPDATE onderzoek SET aanta5 = %s where key_column = %s", (y,x))
        if (x%5)==0:
            y=y+1
y=1
for x in range(1, 100):
        cur.execute("UPDATE onderzoek SET aanta6 = %s where key_column = %s", (y,x))
        if (x%6)==0:
            y=y+1

conn.commit()

rows = cur.execute('SELECT * FROM onderzoek GROUP BY key_column LIMIT 100')
df = pandas.DataFrame(cur.fetchall(), columns = ['address', 'inwoners2015', 'hn_p99', 'oppervl', 'volume', 'lengte', 'geom', 'key_column', 'aanta2', 'aanta3', 'aanta4', 'aanta5', 'aanta6'])




print (df)
conn.commit()