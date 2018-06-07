import re
from pprint import pprint
from typing import List, Tuple, NewType

import requests
from bs4 import BeautifulSoup, Tag
from django import db  # Used for transaction.atomic
from django.contrib.postgres import search  # Used for SearchVector
from django.core.management import base

from goodbullapi.management.commands import \
    _common_functions as common_functions

BASE_URL = "http://catalog.tamu.edu/"
DEPARTMENT_LIST_URL = BASE_URL + "%s/course-descriptions"
GRADUATE = "graduate"
UNDERGRADUATE = "undergraduate"

CourseFields = NewType("CourseFields", (str, str, int, int, str, str, str))


def collect_departments(dept_list_html: BeautifulSoup) -> List[Tuple[str, str]]:
    """Given html from dept list page, extract all depts listed and their urls.

    Args:
        dept_list_html: The HTML from the department list page, as a BeautifulSoup instance.
    Returns:
        A list of tuples of format (URL path, dept abbreviation)
    """
    a_elements = dept_list_html.select("#atozindex > ul > li > a")
    url_dept_pairs = []
    for a in a_elements:
        try:
            ABBR_PATTERN = re.compile("(?P<dept>^[a-zA-Z]{3,4})")
            dept_abbr = re.findall(ABBR_PATTERN, a.text)[0]
            url_dept_pairs.append((a["href"], dept_abbr))
        except Exception as e:
            pprint(a)
            raise e
    return url_dept_pairs


def sanitize(string: str) -> str:
    """Takes a string and replaces Unicode characters with single spaces."""
    return ''.join([i if ord(i) < 128 else ' ' for i in string])


def parse_courseblocktitle(courseblocktitle: BeautifulSoup) -> Tuple[str, str]:
    """Parses the course number and course name from a .courseblocktitle element.
    
    Args:
        courseblocktitle: A BeautifulSoup instance around the .courseblocktitle element of a .courseblock elem.
    Returns:
        A tuple of format ("Course number", "Course name").
    """
    COURSE_NUM_NAME_PATTERN = re.compile(
        "(?:[a-zA-Z]{3,4}[0-9]?) (?P<course_num>[0-9]{3,4}[a-zA-Z]?) (?P<name>.*)")
    title_text = courseblocktitle.select_one('strong').text
    title_text = sanitize(title_text)
    return re.findall(COURSE_NUM_NAME_PATTERN, title_text)[0]


def parse_courseblock(courseblock: BeautifulSoup) -> CourseFields:
    """Parses a .courseblock element and returns all important information.

    Args:
        courseblock: A BeautifulSoup instance around a .courseblock element.
    Returns:
        A CourseFields (see above definition)
    """
    courseblocktitle = courseblock.select_one('.courseblocktitle')
    course_num, name = parse_courseblocktitle(courseblocktitle)


class Command(base.BaseCommand):
    def handle(self, *args, **options):
        education_levels = [UNDERGRADUATE, GRADUATE]
        for level in education_levels:
            description_url = DEPARTMENT_LIST_URL % level
            course_description_html = common_functions.request_html(
                description_url)
            url_dept_pairs = collect_departments(course_description_html)
