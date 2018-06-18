import codecs
import csv
import re
import urllib

from django.contrib.postgres.search import SearchVector
from django.core.management.base import BaseCommand
from django.db import transaction

from goodbullapi.models import Building

BUILDING_CSV = 'http://fcor.tamu.edu/webreporter/exportv6.asp?fm=2&t=[Current_Inv_Bldgs]&strSQL=Select%20[BldgAbbr],%20[BldgName],%20[LocDesc],%20[YearBuilt],%20[NumFloors],%20[Address],%20[City],%20[Zip]%20From%20[Current_Inv_Bldgs]%20Where%20BldgAbbr%20Like%20~^^~'


class Command(BaseCommand):
    help = 'Retrieves all of the buildings in the Texas A&M University system'

    def stream_csv(self, url: str):
        """
        A generator function that takes a URL pointing to a CSV,
        and yields each non-header row of the CSV.

        Args:
            url: The URL pointing to a CSV file.
        Yields:
            A row from the CSV.
        """
        file_stream = urllib.request.urlopen(url)
        csvfile = csv.reader(codecs.iterdecode(file_stream, 'utf-8'))
        next(csvfile)
        for row in csvfile:
            yield row

    @transaction.atomic
    def handle(self, *args, **options):
        for row in self.stream_csv(BUILDING_CSV):
            # This CSV for some reason include blanks at the end of each row.
            row = row[:8]

            abbreviation, name, location_desc, year_built, num_floors, address, city, zip_code = row
            if not year_built:
                year_built = None
            else:
                year_built = int(year_built)
            if not num_floors:
                num_floors = None
            else:
                num_floors = int(num_floors)

            searchable_string = '{} {}'.format(abbreviation, name)
            b = Building(abbr=abbreviation, 
                         name=name, 
                         location_description=location_desc,
                         year_built=year_built, 
                         num_floors=num_floors, 
                         address=address, 
                         city=city, 
                         zip_code=zip_code, 
                         searchable_field=searchable_string
                        )
            b.save()
        Building.objects.update(search_vector=SearchVector('searchable_field'))
        self.stdout.write('Finished scraping buildings.')
