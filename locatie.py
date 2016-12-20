#!/usr/bin/python

from geopy.geocoders import GoogleV3
geolocator = GoogleV3()
import psycopg2
conn = psycopg2.connect(dbname="crest", port=5432, user="samuel",
                            password="samuvack", host="we12s300.ugent.be")

print ("Opened database successfully")

cur = conn.cursor()

for rij in range(1,100000):

        cur.execute(
            'SELECT streetnl  FROM adres WHERE key_column = (%(row)s)',
            {'row': rij})

        #cur.execute('''SELECT streetnl  FROM adress LIMIT 1;''')

        street = cur.fetchone()
        cur.execute(
            'SELECT housenumber  FROM adres WHERE key_column = (%(row)s)',
            {'row': rij})

        number = cur.fetchone()

        cur.execute(
            'SELECT municipalitynl  FROM adres WHERE key_column = (%(row)s)',
            {'row': rij})

        municipality = cur.fetchone()

        cur.execute(
            'SELECT box  FROM adres WHERE key_column = (%(row)s)',
            {'row': rij})

        box = cur.fetchone()
        if box[0] is None:
                test=" "
        else:
                test = box[0]

        cur.execute(
            'SELECT zipcode  FROM adres WHERE key_column = (%(row)s)',
            {'row': rij})
        zipcode = cur.fetchone()

        s = " ";
        seq = (street[0], number[0], test[0], ",", zipcode[0], municipality[0], "Belgium"); # This is sequence of strings.

        location = geolocator.geocode(s.join(seq))


        xvar = location.latitude
        yvar = location.longitude


        cur.execute(
            'UPDATE adres SET x = (%(xvar)s) WHERE key_column = (%(row)s);',
            {'xvar': xvar, 'row': rij})
        #cur.fetchone()

        cur.execute(
            'UPDATE adres SET y = (%(yvar)s) WHERE key_column = (%(row)s);',
            {'yvar': yvar,'row': rij})
        #cur.fetchone()

        print (rij)




conn.commit()
conn.close()
