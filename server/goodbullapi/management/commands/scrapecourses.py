from bs4 import BeautifulSoup
from django.contrib.postgres.search import SearchVector
from django.core.management.base import BaseCommand
from django.db import transaction

from goodbullapi.models import Building, Course

from ._functions.functions import (parse_course_block, request_catalog_depts,
                                   request_html)


class Command(BaseCommand):
    help = 'Retrieves all of the courses in the Texas A&M University system'

    @transaction.atomic
    def handle(self, *args, **options):
        UNDERGRADUATE = 'undergraduate'
        GRADUATE = 'graduate'
        education_levels = [UNDERGRADUATE, GRADUATE]
        for edu_lvl in education_levels:
            for abbr, url in request_catalog_depts(edu_lvl):
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
                        searchable_field = '{} {} {}'.format(
                            abbr, course_num, title)
                        c = Course(_id=_id, dept=abbr, course_num=course_num, name=title, min_credits=min_credits, max_credits=max_credits,
                                   distribution_of_hours=distribution_of_hours, description=description, prereqs=prereqs, coreqs=coreqs, searchable_field=searchable_field)
                        c.save()
        Course.objects.update(
            search_vector=SearchVector('searchable_field'))
