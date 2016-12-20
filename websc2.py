#!/usr/bin/env python
import demjson
import requests
from bs4 import BeautifulSoup
import re
import urllib
import psycopg2

pand_list = list()

i = 0
while True:
    i += 1
    print('Scraping page {}.'.format(i))
    url = "http://www.zimmo.be/nl/panden/?status=1&hash=8ae2f0686cb9464bd18c104ee7c17252&priceIncludeUnknown=1&priceChangedOnly=0&bedroomsIncludeUnknown=1&bathroomsIncludeUnknown=1&constructionIncludeUnknown=1&livingAreaIncludeUnknown=1&landAreaIncludeUnknown=1&commercialAreaIncludeUnknown=1&yearOfConstructionIncludeUnknown=1&epcIncludeUnknown=1&queryCondition=and&includeNoPhotos=1&includeNoAddress=1&onlyRecent=0&onlyRecentlyUpdated=0&isPlus=0&region=list&district=MzAYBaOAADAEAA%253D%253D{}#gallery".format(i)
    url1 = url
    request1 = requests.get(url1)
    table = BeautifulSoup(request1.text, "html.parser")
    panden = table.select('[id^=pand]')
    if len(panden) == 0:
        break

    for pand in panden:
        detail_url = "http://www.zimmo.be" + pand.select('a.detail')[0]['href']

        request1 = requests.get(detail_url)
        table = BeautifulSoup(request1.text, "html.parser")
        feature_labels = table.select(".feature-label")
        for label in feature_labels:
            if label.text.strip() == 'KI':
                ki = label.parent.select('.feature-value')[0].text[4:]
            else : ki = None
        table = str(table)
        afstand = table.find("property: {")
        afstand2 = table.find("sellerType")
        properties = demjson.decode(table[afstand:afstand2].strip()[10:-1])
        properties = {**{
            'epc': None,
            'lat': None,
            'lon': None,
            'bouwjaar': None,
            'woonopp': None,
            'grondopp': None,
            'aantal_slaapkamers': None,
            'prijs': None,
            'address': None,
            'gemeente': None,
            'postcode': None
        }, **properties}

        epc = properties['epc']
        lat = properties['lat']
        lon = properties['lon']
        bouwjaar = properties['bouwjaar']
        woonopp = properties['woonopp']
        grondopp = properties['grondopp']
        slaapkamers = properties['aantal_slaapkamers']

        prijs = properties['prijs']
        # adres
        adres = properties['address']
        gemeente = properties['gemeente']
        postcode = properties['postcode']
        pand_id = pand['id'][5:]

        pand_list.append({
            'id': pand_id,
            'slaapkamers': slaapkamers,
            'adres': adres,
            'prijs': prijs,
            'postcode': postcode,
            'gemeente': gemeente,
            'grondopp': grondopp,
            'epc': epc,
            'lat': lat,
            'lon': lon,
            'bouwjaar': bouwjaar,
            'woonopp': woonopp,
            'ki' : ki
        })
        print("Scraped")

print(pand_list)

hostname = 'we12s300.ugent.be'
username = 'samuel'
password = 'samuvack'
database = 'zimmo'

# Try to connect

try:
    conn = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
except:
    print("I am unable to connect to the database.")

cur = conn.cursor()
for pand in pand_list:
    cur.execute(
        'INSERT INTO zimmo_aalst_woningen VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO UPDATE SET oppervlakte = excluded.oppervlakte, slaapkamers=excluded.slaapkamers, prijs=excluded.prijs, adres=excluded.adres, postcode=excluded.postcode, gemeente=excluded.gemeente, epc = excluded.epc, lat = excluded.lat, lon = excluded.lon, bouwjaar = excluded.bouwjaar, woonopp = excluded.woonopp, ki = excluded.ki',
        (pand['id'], pand['grondopp'], pand['slaapkamers'], pand['prijs'], pand['adres'], pand['postcode'],
         pand['gemeente'], pand['epc'], pand['lat'], pand['lon'], pand['bouwjaar'], pand['woonopp'], pand['ki']))
conn.commit()