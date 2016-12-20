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

rows = cur.execute('SELECT * FROM inwoners_gent LIMIT 100')
#df = pandas.DataFrame(cur.fetchall(), columns = ['gid', 'straatkode', 'nr_oud', 'in_oud', 'geslacht', 'lft', 'koppeladr'])



from toolz import partition_all, concat
partitions = partition_all(10000, rows)

from dask.distributed import Executor
e = Executor('scheduler-address:8786')

futures = []

for part in partitions:
    x = e.submit(tokenize, part)
    y = e.submit(process, x)
    futures.append(y)

results = e.gather(futures)
result = list(concat(results))

print(result)




print (df)
conn.commit()

