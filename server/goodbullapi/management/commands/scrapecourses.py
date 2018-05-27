import re
from pprint import pprint

from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from django.db import transaction

from goodbullapi.models import Course

from ._functions.functions import (parse_course_block, parse_credits,
                                   parse_title, request_catalog_departments,
                                   request_html, sanitize)


class Command(BaseCommand):
    help = 'Retrieves all of the courses in the Texas A&M University course catalogs'

    @transaction.atomic
    def handle(self, *args, **options):
        UNDERGRADUATE = 'undergraduate'
        GRADUATE = 'graduate'
        education_levels = [UNDERGRADUATE, GRADUATE]
        for edu_lvl in education_levels:
            for abbr, url in request_catalog_departments(edu_lvl):
                print(abbr)
                html = request_html(url)
                soup = BeautifulSoup(html, 'lxml')
                course_blocks = soup.select('.courseblock')
                for course_block in course_blocks:
                    results = parse_course_block(course_block)
                    if results:
                        course_num, title, min_credits, max_credits, distribution_of_hours, description, prereqs, coreqs = results
                        _id = '{dept}_{course_num}'.format(
                            dept=abbr, course_num=course_num)
                        c = Course(_id=_id, dept=abbr, course_num=course_num, name=title, min_credits=min_credits, max_credits=max_credits,
                                   distribution_of_hours=distribution_of_hours, description=description, prereqs=prereqs, coreqs=coreqs)
                        try:
                            c.save()
                        except Exception as e:
                            pprint(c.__dict__)
                            lengths = {}
                            for key in c.__dict__:
                                if isinstance(c.__dict__[key], str):
                                    lengths[key] = len(c.__dict__[key])
                            pprint(lengths)
                            raise e
