import os
import re
import sys

import django
import requests
from bs4 import BeautifulSoup
from django.db import transaction

from common_functions import get_depts, get_term_codes


sys.path.append(
    os.path.realpath(
        os.path.join(
            os.path.dirname(__file__),
            '../server/')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

from goodbullapi.models import Course

@transaction.atomic
def collect(dept, term_code):
    URLS = [
        'http://catalog.tamu.edu/undergraduate/course-descriptions/',
        'http://catalog.tamu.edu/graduate/course-descriptions/'
    ]

    for url in URLS:
        url = url + dept.lower()
        r = requests.get(url)
        # Sometimes a course is offered to undergrads and not grads, & vice
        # versa
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            courses = soup.find_all(class_='courseblock')
            for course in courses:
                title = course.find(class_='courseblocktitle').text
                split_title = re.split(r'[\W]', title)

                # Get the course number (as it's offered in this department)
                course_num = split_title[1]

                # Sometimes a course if offered in multiple departments, avoid
                # including the other departments
                if '/' in title:
                    split_title = split_title[4:]

                # Build the formal course name
                name = ' '.join(split_title[2:]).strip()
                name = re.sub(' +', ' ', name)
                if len(name) > 100:
                    print(name)
                hours = course.find(class_='hours').text
                credits = hours[0]
                split_hours = hours.split('. ')

                # Get the number of credit hours
                if 'to' in hours or '-' in hours:
                    credits = -1
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
                    credits=credits,
                    name=name,
                    description=description,
                    division_of_hours=dist_hours,
                    prereqs=prereqs,
                    term_code=term_code
                )
                course.save()
    print(dept)


term_codes = get_term_codes()
for term_code in term_codes:
    depts = get_depts(term_code)
    for dept in depts:
        collect(dept, term_code)
