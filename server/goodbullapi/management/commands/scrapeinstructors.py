import re
from pprint import pprint

from bs4 import BeautifulSoup
from django.contrib.postgres.search import SearchVector
from django.core.management.base import BaseCommand
from django.db import transaction

from goodbullapi.models import Instructor

from ._functions.functions import request_catalog_instructors


class Command(BaseCommand):
    help = 'Retrieves all of the instructors in the Texas A&M University course catalogs'

    @transaction.atomic
    def handle(self, *args, **options):
        for lastname, firstname in request_catalog_instructors():
            fullname = firstname + " " + lastname
            instructor = Instructor(
                lastname=lastname, firstname=firstname, searchable_field=fullname)
            instructor.save()
        Instructor.objects.update(
            search_vector=SearchVector('searchable_field'))
        self.stdout.write('Finished creating skeletons')
