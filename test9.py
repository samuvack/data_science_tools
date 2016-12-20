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


conn.commit()

rows = cur.execute('SELECT * FROM onderzoek GROUP BY key_column')
df = pandas.DataFrame(cur.fetchall(), columns = ['address', 'inwoners2015', 'hn_p99', 'oppervl', 'volume', 'lengte', 'geom', 'key_column', 'aanta2', 'aanta3', 'aanta4', 'aanta5', 'aanta6'])

y=1
for x in range(1, 103985):
        cur.execute("UPDATE onderzoek SET aanta6 = %s where key_column = %s", (y,x))
        if (x%6)==0:
            y=y+1


print (df)
conn.commit()