
hostname = 'we12s300.ugent.be'
username = 'samuel'
password = 'samuvack'
database = 'fliat'

import json
import urllib
import psycopg2
import time
from tqdm import *


# Try to connect

try:
    conn = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
except:
    print ("I am unable to connect to the database.")

cur = conn.cursor()
cur.execute('''SELECT distinct(werknemers) from "4_kbo_grb_ghent"''')
row = [item[0] for item in cur.fetchall()]
conn.commit()

#row[] = row[].replace("'", "")

for i in range(1,len(row)-1):
    row[i] = row[i].replace("'", "")

for x in range(1, len(row)-1):
    cur.execute("insert INTO onderneming (werknemer2) VALUES  (%s)", (row[x]))
conn.commit()

#onderneming = onderneming.replace(" ", "")