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
        'INSERT INTO zimmo_kust_test VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO UPDATE SET oppervlakte = excluded.oppervlakte, slaapkamers=excluded.slaapkamers, prijs=excluded.prijs, adres=excluded.adres, postcode=excluded.postcode, gemeente=excluded.gemeente, epc = excluded.epc, lat = excluded.lat, lon = excluded.lon, bouwjaar = excluded.bouwjaar, woonopp = excluded.woonopp, grondopp = excluded.grondopp, ki = excluded.ki',
        (pand['id'], pand['grondopp'], pand['slaapkamers'], pand['prijs'], pand['adres'], pand['postcode'],
         pand['gemeente'], pand['epc'], pand['lat'], pand['lon'], pand['bouwjaar'],pand['grondopp'], pand['woonopp'], pand['ki']))
conn.commit()