from django.core.management.base import BaseCommand
from django.db import transaction
from ._functions import request_catalog_departments, request_html
import re
from bs4 import BeautifulSoup

COURSENUM_TITLE_PATTERN = re.compile(
    '(?P<course_num>[0-9]{3,4}|[0-9]{3}[a-zA-Z]{1}) (?P<name>.+)')


class Command(BaseCommand):
    help = 'Retrieves all of the courses in the Texas A&M University course catalogs'

    def parse_title(self, course_block_title_text):
        return re.findall(
            COURSENUM_TITLE_PATTERN, course_block_title_text)[0]

    @transaction.atomic
    def handle(self, *args, **options):
        UNDERGRADUATE = 'undergraduate'
        GRADUATE = 'graduate'
        education_levels = [UNDERGRADUATE, GRADUATE]
        for edu_lvl in education_levels:
            for abbr, url in request_catalog_departments(edu_lvl):
                html = request_html(url)
                soup = BeautifulSoup(html, 'lxml')
                course_blocks = soup.select('.courseblock')
                for course_block in course_blocks:
                    course_block_title_text = course_block.select_one(
                        '.courseblocktitle').get_text()
                    course_num, title = self.parse_title(course_block_title_text)
