import re

import requests

import helpful_regex
import sync_with_django_orm
from bs4 import BeautifulSoup
from common_functions import request_depts, request_term_codes
from django.db import transaction
from goodbullapi.models import Course
from rest_framework import status


def request_html(url):
    r = requests.get(url)
    if r.status_code == status.HTTP_200_OK:
        return r.text
    elif r.status_code == status.HTTP_404_NOT_FOUND:
        # It's okay to not find a page. This means that
        # the department is not offered to graduates/undergraduates
        # (depends on the url)
        return None
    else:
        r.raise_for_status()


def extract_course_title(course_block_title_text):
    return re.findall(helpful_regex.COURSE_EXTRACT_TITLE, course_block_title_text)[0]


@transaction.atomic
def collect(dept, term_code):
    URLS = [
        'http://catalog.tamu.edu/undergraduate/course-descriptions/',
        'http://catalog.tamu.edu/graduate/course-descriptions/'
    ]

    for base_url in URLS:
        url = base_url + dept.lower()
        page_html = request_html(url)
        if page_html:
            soup = BeautifulSoup(page_html, 'html.parser')
            courses = soup.find_all(class_='courseblock')
            for course in courses:
                course_block_title_text = course.find(
                    class_='courseblocktitle').text
                title = extract_course_title(course_block_title_text)
                
                hours = course.find(class_='hours').text
                credits = hours[0]
                split_hours = hours.split('. ')

                # Get the number of credit hours
                if 'to' in hours or '-' in hours:
                    credits = None
                else:
                    credits = int(
                        hours[hours.index(' '):hours.index('.')].strip())

                # Get how much time is spent in lecture, lab, etc.
                dist_hours = '. '.join(split_hours[1:]).strip()

                # Get course description
                description = course.find(
                    class_='courseblockdesc').text.strip()

                # Get the prerequsites/corequisites of this course
                prereqs = None
                if 'Prerequisite:' in description:
                    prereqs = description[description.index(
                        'Prerequisite:') + len('Prerequisite:'):].strip()
                elif 'Prerequisites:' in description:
                    prereqs = description[description.index(
                        'Prerequisites:') + len('Prerequisites:'):].strip()
                if prereqs:
                    description = description[0:description.index(prereqs)]
                _id = '{}_{}_{}'.format(dept, course_num, term_code)
                course = Course(
                    _id=_id,
                    dept=dept,
                    course_num=course_num,
                    least_credits=credits,
                    most_credits=credits,
                    name=name,
                    description=description,
                    division_of_hours=dist_hours,
                    prereqs=prereqs,
                    term_code=term_code
                )
                course.save()
    print(dept)


for term_code in request_term_codes():
    for dept in request_depts(term_code):
        collect(dept, term_code)
