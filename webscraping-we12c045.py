#https://docs.python.org/3/library/urllib.request.html#urllib.request.urlopen

#library---------------------------------------------------------------------------------------------

import urllib.request
with urllib.request.urlopen("http://www.python.org") as url:
    s = url.read()

#output the html source code?
print(s)


print(s[0])