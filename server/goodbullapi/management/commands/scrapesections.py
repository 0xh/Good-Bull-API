import re
from pprint import pprint

from bs4 import BeautifulSoup
from django.contrib.postgres.search import SearchVector
from django.core.management.base import BaseCommand
from django.db import transaction

from ._functions.functions import request_compass_term_codes, request_compass_depts, request_compass_sections


class Command(BaseCommand):
    help = 'Scrapes all of the sections on Howdy. Two modes: \nrecurring: Only scrapes the top 10 terms (used for updating the current terms for instructor/location changes)\ndeep: Scrapes all of the terms to populate the database.'

    @transaction.atomic
    def handle(self, *args, **options):
        for term_code in request_compass_term_codes(full_scrape=True):
            for dept in request_compass_depts(term_code):
                request_compass_sections(dept, term_code)
