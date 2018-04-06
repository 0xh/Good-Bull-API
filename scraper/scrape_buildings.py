import django
import os
import sys
import csv
import urllib.request
import codecs
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../server/')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

from buildings.models import Building

url = 'http://fcor.tamu.edu/webreporter/exportv6.asp?fm=2&t=[Current_Inv_Bldgs]&strSQL=Select%20[BldgAbbr],%20[BldgName],%20[Address],%20[City],%20[Zip]%20From%20[Current_Inv_Bldgs]%20Where%20BldgAbbr%20Like%20~^^~'

ftpstream = urllib.request.urlopen(url)
csvfile = csv.reader(codecs.iterdecode(ftpstream, 'utf-8'))

for line in csvfile:
    b = Building(abbr=line[0], name=line[1], address=line[2], city=line[3], zip_code=line[4])
    b.save()

