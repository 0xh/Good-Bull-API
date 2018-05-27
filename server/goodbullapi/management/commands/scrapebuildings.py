from django.core.management.base import BaseCommand, CommandError
from goodbullapi.models import Building
from django.db import transaction
from django.contrib.postgres.search import SearchVector

from ._common_functions import stream_csv


class Command(BaseCommand):
    help = 'Retrieves all of the buildings in the Texas A&M University system'

    @transaction.atomic
    def handle(self, *args, **options):
        BUILDING_CSV = 'http://fcor.tamu.edu/webreporter/exportv6.asp?fm=2&t=[Current_Inv_Bldgs]&strSQL=Select%20[BldgAbbr],%20[BldgName],%20[LocDesc],%20[YearBuilt],%20[NumFloors],%20[Address],%20[City],%20[Zip]%20From%20[Current_Inv_Bldgs]%20Where%20BldgAbbr%20Like%20~^^~'
        for row in stream_csv(BUILDING_CSV):
            # CSV rows for some reason include blanks at the end of each row.
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
            b = Building(abbr=abbreviation, name=name, location_description=location_desc,
                         year_built=year_built, num_floors=num_floors, address=address, city=city, zip_code=zip_code, searchable_field=searchable_string)
            b.save()
        Building.objects.update(search_vector=SearchVector('searchable_field'))
        self.stdout.write('Finished scraping buildings.')
