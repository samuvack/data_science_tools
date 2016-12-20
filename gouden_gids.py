#!/usr/bin/env python
import demjson
import requests
from bs4 import BeautifulSoup
import re
import urllib
import psycopg2




i=1
url = "http://www.goudengids.be/artsen/{}/".format(i)
url1 = url
request1 = requests.get(url1)
table = BeautifulSoup(request1.text, "html.parser")
#print(table)

mydivs = table.findAll("div", { "class" : "highlightable" })
print(mydivs)