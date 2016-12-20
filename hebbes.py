#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup
import psycopg2

pand_list = list()

i = 21
while True:
    i += 1
    page_url = 'http://www.hebbes.be/immo?DestID=1&Nat=True&Zips=2470&Ord=7&Offset=504&Catgs=3,4,5,8,9,-3,-4&ForMap=False&IsBasic=True&page={}'.format(i)
    page_request = requests.get(page_url)
    page = BeautifulSoup(page_request.text, "html.parser")

    panden = page.select('.adds-link-wrap')
    if len(panden) == 0:
        break

    for pand in panden:
        detail_url = pand['href']
        detail_request = requests.get(detail_url)
        details = BeautifulSoup(detail_request.text, 'html.parser')

        properties = {
                'prijs': details.select_one('.detail-compact__price').text,
                'data': details.select_one('.detail-compact__data span').text,
                'adres': details.select_one('.detail-compact__location span').text
        }

        #print(properties)
        pand_list.append(properties)
        print(properties['adres'])
        print(properties['data'])
        afstand = properties['data'].find("slpk")
        if afstand == -1:
            #print("niets")
            #print(properties['data'][0:afstand])
            slaapkamer = None
        else :
            #print(properties['data'][0:afstand+4])
            slaapkamer = properties['data'][0:afstand]

        afstand = properties['data'].find("bewoonbare")
        if afstand == -1:
            #print("niets")
            #print(properties['data'][0:afstand])
            bebouwde = None
        else:
            #print(properties['data'][7:afstand-4])
            bebouwde = properties['data'][7:afstand-4]



print(pand_list)
#-----------------------------------------------------------------------
'''
hostname = 'we12s300.ugent.be'
username = 'samuel'
password = 'samuvack'
database = 'zimmo'

# Try to connect

try:
    conn = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
except:
    print ("I am unable to connect to the database.")

cur = conn.cursor()
for pand in pand_list:
    cur.execute('INSERT INTO hebbes_kust_woningen VALUES (%s, %s, %s, %s, %s, %s,%s) ON CONFLICT (id) DO UPDATE SET oppervlakte = excluded.oppervlakte, slaapkamers=excluded.slaapkamers, prijs=excluded.prijs, adres=excluded.adres, postcode=excluded.postcode, gemeente=excluded.gemeente', (pand['id'], pand['grondopp'], pand['slaapkamers'], pand['prijs'], pand['adres'], pand['postcode'], pand['gemeente']))
conn.commit()
'''
