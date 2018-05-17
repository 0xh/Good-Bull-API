import codecs
import csv
import urllib.request

import sync_with_django_orm

from goodbullapi.models import Building


url = 'http://fcor.tamu.edu/webreporter/exportv6.asp?fm=2&t=[Current_Inv_Bldgs]&strSQL=Select%20[BldgAbbr],%20[BldgName],%20[Address],%20[City],%20[Zip]%20From%20[Current_Inv_Bldgs]%20Where%20BldgAbbr%20Like%20~^^~'

ftpstream = urllib.request.urlopen(url)
csvfile = csv.reader(codecs.iterdecode(ftpstream, 'utf-8'))

for line in csvfile:
    abbreviation, name, address, city, zip_code = line[:5]
    b = Building(
        abbr=abbreviation,
        name=name,
        address=address,
        city=city,
        zip_code=zip_code)
    b.save()
