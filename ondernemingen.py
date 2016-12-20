werknemers_list = list()
inschrijvingsdatum_list = list()
onderneming_list = list()

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
cur.execute('''SELECT distinct(entitynumber) from "4_kbo_grb_ghent"''')
row = [item[0] for item in cur.fetchall()]
conn.commit()
for i in range(0,len(row)-1):
    row[i] = row[i].replace('.', "")
#print(row[2])

#-----------------------------------------------------------------------------------------------------------------

import requests
from bs4 import BeautifulSoup


for i in tqdm(range(0, len(row))):
        url1 = 'https://www.socialsecurity.be/app014/wrep/rep_gp.do?language=nl&REP_KEY_VALUE={}&ACCESS_TYPE=0&ACTION=1&REP_KEY_TYPE=12&REP_LIMIT_DATE'.format(row[i])
        url2 = 'https://www.socialsecurity.be/app014/wrep/rep/gp/jsp/nl/REPGPdata.jsp'
        request1 = requests.get(url1)
        request2 = requests.get(url2, cookies = request1.cookies)
        #print (row[i])
        onderneming_list.append(row[i])
        table = str(request2.text)
        #print(table)

        afstand = table.find("Belangrijkheidscode")
        afstand2 = table.find("Bijwerking")
        werknemers = table[afstand+60:afstand2-47]

        afstand = table.find("Inschrijvingsdatum")
        afstand2 = table.find("Schrappingsdatum")
        inschrijvingsdatum = table[afstand+60:afstand2-42]


        #print(werknemers)
        #print(inschrijvingsdatum)

        #afstand = table.find("economicActivitiesDataForm")
        #nace = table[afstand+225:afstand+230]

        '''
        url1 = 'http://kbopub.economie.fgov.be/kbopub/toonondernemingps.html?ondernemingsnummer={}'.format(row[i])

        request1 = requests.get(url1)

        table = str(request1.text)
        #print(request1.text)



        afstand = table.find("nace.code")
        nace = table[afstand+10:afstand+15]


        #print(nace)
        '''

        #nace_list.append(nace)
        werknemers_list.append(werknemers)
        inschrijvingsdatum_list.append(inschrijvingsdatum)

print(werknemers_list)
#print(nace_list)


#--------------------------------------------------------------------------------------------------------------------
conn = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
cur = conn.cursor()
for i in range(0, len(werknemers_list)):
    cur.execute("insert INTO onderneming VALUES (%s, %s,%s) ",(onderneming_list[i], inschrijvingsdatum_list[i], werknemers_list[i]))

conn.commit()
