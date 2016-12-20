#!/usr/bin/env python
import demjson
import requests
from bs4 import BeautifulSoup
import re
import urllib
import psycopg2




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


cur.execute('SELECT * FROM zimmo_gent_woningen')


#for pand in pand_list:
#    cur.execute('INSERT INTO zimmo_gent_woningen VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, %s, %s, %s) ON CONFLICT (id) DO UPDATE SET oppervlakte = excluded.oppervlakte, slaapkamers=excluded.slaapkamers, prijs=excluded.prijs, adres=excluded.adres, postcode=excluded.postcode, gemeente=excluded.gemeente, epc = excluded.epc, lat = excluded.lat, lon = excluded.lon, bouwjaar = excluded.bouwjaar, woonopp = excluded.woonopp, grondopp = excluded.grondopp, ki = excluded.ki, tijd= CURRENT_TIMESTAMP, subtype = excluded.subtype, type = excluded.type, zmvPrijs = excluded.zmvPrijs', (pand['id'], pand['grondopp'], pand['slaapkamers'], pand['prijs'], pand['adres'], pand['postcode'], pand['gemeente'], pand['epc'], pand['lat'], pand['lon'], pand['bouwjaar'],pand['grondopp'], pand['woonopp'], pand['ki'], pand['subtype'], pand['type'], pand['zmvPrijs']))
conn.commit()