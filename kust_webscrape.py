#----------------------------------------------------------------------------------------------------------------
import requests
from bs4 import BeautifulSoup
import re


def num_there(s):
    return any(i.isdigit() for i in s)


id_list = list()
oppervlakte_list = list()
slaapkamers_list = list()
prijs_list = list()
straatnaam_list = list()
nummer_list = list()
postcode_list = list()
gemeente_list = list()



def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

for i in range (1,53):
    pagina = i
    url = "http://www.zimmo.be/nl/panden/?status=1&type%5B0%5D=5&hash=86c443f7d824f3e29fb8377485e15a2c&priceIncludeUnknown=1&priceChangedOnly=0&bedroomsIncludeUnknown=1&bathroomsIncludeUnknown=1&constructionIncludeUnknown=1&livingAreaIncludeUnknown=1&landAreaIncludeUnknown=1&commercialAreaIncludeUnknown=1&yearOfConstructionIncludeUnknown=1&epcIncludeUnknown=1&queryCondition=and&includeNoPhotos=1&includeNoAddress=0&onlyRecent=0&onlyRecentlyUpdated=0&isPlus=0&region=list&district=MzAYBcMGGKICbOIgHkIcVTcVHAAA&pagina={}#gallery".format(pagina)
    url1 = url
    request1 = requests.get(url1)
    #request2 = requests.get(url2, cookies = request1.cookies)


    table = BeautifulSoup(request1.text, "html.parser")
    table = str(table)
    #print(table)

    print(table.count("id=\"pand-"))
    stop = table.count("id=\"pand-")


    for x in range (1, stop):
        #print(table)
        #rows = table.findAll('class')[2::3]
        eerste = find_nth(table, "id=\"pand-", x)
        tweede = find_nth(table, "id=\"pand-", x+1)
        list = table[eerste:tweede]
        #print(list)
        #list = table.find("div", attrs={"class":"item "})
        list = str(list)

        #id
        list1 = list.split('\n', 1)[0]
        id = list1[9:19]
        #print(list1)
        id = id.replace('>', '')
        id = id.replace('"', '')
        print(id)
        #oppervlakte
        afstand = list.find("home_breadcrumbs")
        oppervlakte = list[afstand+23:afstand+26]
        print(oppervlakte)

        #aantal slaapkamers
        afstand = list.find("icon-bed")
        slaapkamer = list[afstand+14:afstand+16]
        print(slaapkamer)

        #prijs
        afstand = list.find("â‚¬ \d")
        prijs= list[afstand+3:afstand+12]
        print(prijs)

        #prijs
        afstand = list.find("â¬")
        prijs2= list[afstand+3:afstand+12]
        prijs2 = prijs2.replace('.', "")
        prijs2 = prijs2.replace(" ","")
        print(prijs2)


        #adres
        afstand= list.find("address-info")
        afstand2= list.find("z-code")
        adres = list[afstand+14:afstand2-24]
        adres = adres.replace(" ", "")
        #adres = adres.replace('\n', "")
        straat = adres[1:adres.find("<br/>")]

        gemeente = adres[adres.find("<br/>") + 5:len(adres)]
        gemeente = gemeente.replace("/n", "")

        print(straat)
        if num_there(straat):
            for i, c in enumerate(straat):
                if c.isdigit():
                    print(i)
                    plaats = int(i)
                    break

            straatnaam = straat[0:plaats]
            nummer = straat[plaats: len(straat)]
            print(straatnaam)
            print (nummer)
        else:
            straatnaam = straat
            nummer = None
            print(straatnaam)
            print(nummer)

        print(gemeente)
        postcode = gemeente[1:5]
        gemeente = gemeente[5:len(gemeente)]
        print(postcode)
        print(gemeente)


        id_list.append(id)

        if oppervlakte.isnumeric():
            oppervlakte_list.append(oppervlakte)
        else:
            oppervlakte_list.append(0)
        slaapkamers_list.append(slaapkamer)
        prijs_list.append(prijs2)
        straatnaam_list.append(straatnaam)
        nummer_list.append(nummer)
        postcode_list.append(postcode)
        gemeente_list.append(gemeente)
#---------------------------------------------------------------------------------------------------------------
'''
print(straatnaam)
print(len(straatnaam))


print(len(id_list))


hostname = 'we12s300.ugent.be'
username = 'samuel'
password = 'samuvack'
database = 'zimmo'

import json
import urllib
import psycopg2

# Try to connect

try:
    conn = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
except:
    print ("I am unable to connect to the database.")

cur = conn.cursor()
try:
    cur.execute("SELECT * from zimmo_kust_woningen")
except:
    print ("I can't SELECT from 1_ev_car")

for x in range(1, len(id_list)):
    cur.execute("insert INTO zimmo_kust_woningen VALUES  (%s, %s, %s, %s, %s, %s,%s, %s)", (id_list[x], oppervlakte_list[x],slaapkamers_list[x], prijs_list[x], straatnaam_list[x], nummer_list[x], postcode_list[x], gemeente_list[x]))
conn.commit()
cur.execute("DELETE FROM zimmo_kust_woningen WHERE prijs2 LIKE '%pand-21'; ")



conn.commit()

'''