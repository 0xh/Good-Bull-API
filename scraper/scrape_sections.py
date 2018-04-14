import requests
import re
import os
import sys
import django
from datetime import datetime

from common_functions import get_term_codes, get_depts
from bs4 import BeautifulSoup, NavigableString, Tag
from django.db import transaction

sys.path.append(
    os.path.realpath(
        os.path.join(
            os.path.dirname(__file__),
            '../server/')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

from sections.models import Section, Meeting
from courses.models import Course

# Used to emulate an actual person
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
}


"""
    Because of the terrible way that the Howdy portal is written,
    we have to merge the title of a section with its data
    (they're represented in separate rows of the table they're in).
"""


def merge_trs(outer_datadisplaytable):
    trs = outer_datadisplaytable.contents[1:]
    trs = [tr for tr in trs if not isinstance(tr, NavigableString)]
    merged = []
    for tr in trs:
        if tr.select_one('th.ddtitle'):
            merged.append(tr)
        elif tr.select_one('td.dddefault'):
            merged[len(
                merged) - 1] = BeautifulSoup(str(merged[len(merged) - 1]) + str(tr), 'lxml')

    return merged


"""
    Extracts the instructor from Howdy data
"""


def extract_instructor(field_data):
    if 'Instructor:' not in field_data and 'Instructors:' not in field_data:
        return None
    field_data = re.split('\n+', field_data)
    slice_index = 0
    while 'Instructor:' not in field_data[slice_index] and 'Instructors:' not in field_data[slice_index]:
        slice_index += 1
    instructor = field_data[slice_index + 1]
    if '(P)' in instructor:
        instructor = instructor[:-3].strip()
    return ' '.join(instructor.split())


"""
    Extracts the number of credits that this course is worth
    (useful for Special Topics courses)
"""


def extract_credits(field_data):
    field_data = re.split('\n+', field_data)
    credits = None
    for line in field_data:
        if 'Credits' in line:
            credits = line.split('Credits', -1)[0]
    if credits:
        if 'TO' in credits or 'OR' in credits:
            return None
        else:
            return float(credits)
    return credits


"""
    Extracts the information regarding meetings, such as location,
    duration, day, and the type of each meeting.
"""


def extract_meetings(meeting_data):
    if not meeting_data: 
        return None
    trs = meeting_data.select('tr')
    meetings = []
    # The first row of every table is the header row, ignore it.
    for tr in trs[1:]:
        meeting_type, duration, days, location, * \
            rest = [td.get_text() for td in tr.select('td')]
        if days == 'TBA':
            days = None
        start_time = end_time = None
        if duration != 'TBA':
            start_time, end_time = duration.upper().split(' - ')
            start_time = datetime.strptime(start_time, '%I:%M %p')
            end_time = datetime.strptime(end_time, '%I:%M %p')

        # TODO: Introduce locations.
        (meeting, created) = Meeting.objects.get_or_create(meeting_type=meeting_type,
                                                           start_time=start_time,
                                                           end_time=end_time,
                                                           days=days)
        meetings.append(meeting)
    return meetings


"""
    Extracts the important data from a section.
"""


def extract_section_data(section):
    # Get section name, crn, course, and section number from title
    split_title = section.select_one('th.ddtitle').get_text().split(' - ')
    section_num = split_title[-1]
    short = split_title[-2]
    crn = split_title[-3]
    section_name = ' '.join(split_title[0:-3])
    crn = int(crn)
    honors = False
    course_num = short.split(' ')[1]
    if '(Syllabus)' in section_num:
        section_num = section_num[0:4].strip()
    try:
        honors = int(section_num) >= 200 and int(section_num) < 300
    except Exception as e:
        print('Encountered section that isn\'t an integer:', section_num)

    # Get meeting information
    try:
        meeting_data = section.select_one('table.datadisplaytable')
        meetings = extract_meetings(meeting_data)
    except Exception as e:
        print(short)
        raise e

    # Get instructor and credits
    field_data = section.select_one('td.dddefault').get_text().strip()
    instructor = extract_instructor(field_data)
    credits = extract_credits(field_data)
    return crn, section_num, honors, section_name, meetings, course_num, credits


@transaction.atomic
def collect(dept, term_code):
    URL = 'https://compass-ssb.tamu.edu/pls/PROD/bwckschd.p_get_crse_unsec?term_in={}&sel_subj=dummy&sel_day=dummy&sel_schd=dummy&sel_insm=dummy&sel_camp=dummy&sel_levl=dummy&sel_sess=dummy&sel_instr=dummy&sel_ptrm=dummy&sel_attr=dummy&sel_subj={}&sel_crse=&sel_title=&sel_schd=%25&sel_insm=%25&sel_from_cred=&sel_to_cred=&sel_camp=%25&sel_levl=%25&sel_ptrm=%25&sel_instr=%25&sel_attr=%25&begin_hh=0&begin_mi=0&begin_ap=a&end_hh=0&end_mi=0&end_ap=a'.format(
        term_code,
        dept)
    r = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(r.text, 'lxml')
    outer_datadisplaytable = soup.select_one('table.datadisplaytable')
    sections = merge_trs(outer_datadisplaytable)
    for section in sections:
        crn, section_num, honors, section_name, meetings, course_num, credits = extract_section_data(
            section)
        _id = '%s_%s' % (crn, term_code)
        course_id = dept + '_' + str(course_num) + '_' + str(term_code)

        COURSE_DEFAULTS = {
            '_id': course_id,
            'short': dept + '_' + course_num,
            'term_code': term_code,
            'name': section_name.title(),
            'credits': credits,
            'description': None,
            'division_of_hours': None,
            'prereqs': 'None listed. Check Howdy.'
        }

        
        (course, created) = Course.objects.get_or_create(
            _id=course_id, defaults=COURSE_DEFAULTS)

        SECTION_DEFAULTS = {
            '_id': _id,
            'term_code': term_code,
            'crn': crn,
            'section_num': section_num,
            'honors': honors,
            'section_name': section_name,
            'course': course
        }
        (s, created) = Section.objects.update_or_create(term_code=term_code, crn=crn,
                                                        defaults=SECTION_DEFAULTS)
        if meetings:
            s.meetings.set(meetings, clear=True)


term_codes = get_term_codes()
for term_code in term_codes:
    depts = get_depts(term_code)
    for dept in depts:
        collect(dept, int(term_code))
        print(term_code, '-', dept)
