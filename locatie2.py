#!/usr/bin/python

from geopy.geocoders import GoogleV3
geolocator = GoogleV3()

#key = "AIzaSyCVFwJiZIVDDxm_vuv_DiJqueAEKJkkeWY"


import geocoder



import psycopg2
conn = psycopg2.connect(dbname="fliat", port=5432, user="samuel", password="samuvack", host="we12s300.ugent.be")

print ("Opened database successfully")

cur = conn.cursor()

for rij in range(322 ,323):

        cur.execute(
            'SELECT straat  FROM data WHERE key_column = (%(row)s)',
            {'row': rij})

        #cur.execute('''SELECT streetnl  FROM adress LIMIT 1;''')

        street = cur.fetchone()
        cur.execute(
            'SELECT huisnummer  FROM data WHERE key_column = (%(row)s)',
            {'row': rij})

        number = cur.fetchone()

        cur.execute(
            'SELECT gemeente FROM data WHERE key_column = (%(row)s)',
            {'row': rij})

        municipality = cur.fetchone()



        if number[0] is None:
                test2=" "
        elif number[0] == "-":
                test2 = " "
        elif number[0] == "''":
                test2 = " "
        else:
                test2 = number[0]

        cur.execute(
            'SELECT postcode  FROM data WHERE key_column = (%(row)s)',
            {'row': rij})
        zipcode = cur.fetchone()

        s = " ";
        seq = (street[0], test2[0], ",", zipcode[0], municipality[0], "Belgium"); # This is sequence of strings.

        location = geocoder.google(s.join(seq))
        print(location)

        locatie = location.latlng

        xvar = locatie[0]
        yvar= locatie[1]
        print(xvar)

        #yvar = location.longitude


        cur.execute(
            'UPDATE data SET x = (%(xvar)s) WHERE key_column = (%(row)s);',
            {'xvar': xvar, 'row': rij})
        #cur.fetchone()

        cur.execute(
            'UPDATE data SET y = (%(yvar)s) WHERE key_column = (%(row)s);',
            {'yvar': yvar,'row': rij})
        #cur.fetchone()

        print (rij)




conn.commit()
conn.close()
