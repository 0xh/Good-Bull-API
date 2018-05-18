
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup, NavigableString, Tag
from django.db import transaction

import helpful_regex
import sync_with_django_orm
from common_functions import request_depts, request_term_codes
from goodbullapi.models import Course, Meeting, Section

# Used to emulate an actual person
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
}


def is_primary_instructor(instructor):
    """
    If the string "(P)" is present in the string
    provided, this is a primary instructor. The
    (P) tag should be removed.
    """
    return '(P)' in instructor


def instructors_are_listed(text):
    return 'Instructor:' in text or 'Instructors:' in text


def merge_trs(outer_datadisplaytable):
    """
    Because of the terrible way that the Howdy portal is written,
    we have to merge the title of a section with its data
    (they're represented in separate rows of the table they're in).
    """
    trs = outer_datadisplaytable.contents[1:]
    trs = [tr for tr in trs if not isinstance(tr, NavigableString)]
    merged = []
    for tr in trs:
        if tr.select_one('th.ddtitle'):
            merged.append(tr)
        elif tr.select_one('td.dddefault'):
            merged[-1] = BeautifulSoup(str(merged[-1]) + str(tr), 'lxml')
    return merged


def extract_instructor(field_data):
    if not instructors_are_listed(field_data):
        return None
    field_data = re.split('\n+', field_data)
    slice_index = 0
    while not instructors_are_listed(field_data[slice_index]):
        slice_index += 1
    instructor = field_data[slice_index + 1].split(', ')[0].upper()
    if is_primary_instructor(instructor):
        instructor = instructor[:-3].strip()
    instructor = re.split(' +', instructor)
    instructor = instructor[-1] + " " + instructor[0][0]
    return instructor


def extract_credits(field_data):
    """
    Extracts the number of credits that this section is worth
    (useful for Special Topics courses)
    """
    field_data = re.split('\n+', field_data)
    least_credits = most_credits = None
    for line in field_data:
        if 'Credits' in line:
            results = re.findall(helpful_regex.VARYING_CREDITS_PATTERN, line)
            if not results:
                exact_credits = re.findall(
                    helpful_regex.REGULAR_CREDITS_PATTERN, line)[0]
                results = (exact_credits, exact_credits)
            else:
                results = results[0]
            least_credits, most_credits = results
            return float(least_credits), float(most_credits)


def extract_meetings(meeting_data):
    """
    Extracts the information regarding meetings, such as location,
    duration, day, and the type of each meeting.
    """

    if not meeting_data:
        return None
    trs = meeting_data.select('tr')
    meetings = []
    # The first row of every table is the header row, ignore it.
    for tr in trs[1:]:
        meeting_type, duration, days, location = [
            td.get_text() for td in tr.select('td')][:4]
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


def is_honors(section_num):
    """
    An honors section is denoted by a number ranging between 200 and 299 (inclusive). This function will
    throw an error if given a non-integer value (sometimes section numbers have letters in them, for some
    unfathomable reason)
    """
    return int(section_num) >= 200 and int(section_num) < 300


def extract_section_data(section):
    """
    Extracts the Course Registration Number (CRN), section number, section name, meetings, course number,
    credits, and whether this specific section is an honors section or not, from a merged `tr`.
    """
    # Get section name, crn, course, and section number from title
    title_text = section.select_one('th.ddtitle').get_text()
    section_name, crn, dept, course_num, section_num = re.findall(
        helpful_regex.TITLE_PATTERN, title_text)[0]
    honors = False
    try:
        honors = is_honors(section_num)
    except Exception:
        print('Encountered section that isn\'t an integer. This is expected. Section number in question is:', section_num)

    # Get meeting information
    meeting_data = section.select_one('table.datadisplaytable')
    meetings = extract_meetings(meeting_data)

    # Get instructor and credits
    field_data = section.select_one('td.dddefault').get_text().strip()
    least_credits, most_credits = extract_credits(field_data)
    # instructor = extract_instructor(field_data)
    return crn, section_num, honors, section_name, meetings, course_num, least_credits, most_credits


@transaction.atomic
def collect(dept, term_code):
    try:
        URL = 'https://compass-ssb.tamu.edu/pls/PROD/bwckschd.p_get_crse_unsec?term_in={}&sel_subj=dummy&sel_day=dummy&sel_schd=dummy&sel_insm=dummy&sel_camp=dummy&sel_levl=dummy&sel_sess=dummy&sel_instr=dummy&sel_ptrm=dummy&sel_attr=dummy&sel_subj={}&sel_crse=&sel_title=&sel_schd=%25&sel_insm=%25&sel_from_cred=&sel_to_cred=&sel_camp=%25&sel_levl=%25&sel_ptrm=%25&sel_instr=%25&sel_attr=%25&begin_hh=0&begin_mi=0&begin_ap=a&end_hh=0&end_mi=0&end_ap=a'.format(
            term_code,
            dept)
        r = requests.get(URL, headers=HEADERS)
        soup = BeautifulSoup(r.text, 'lxml')
        outer_datadisplaytable = soup.select_one('table.datadisplaytable')
        sections = merge_trs(outer_datadisplaytable)
        for section in sections:
            crn, section_num, honors, section_name, meetings, course_num, least_credits, most_credits = extract_section_data(
                section)
            _id = '%s_%s' % (crn, term_code)
            course_id = '%s_%s_%s' % (dept, course_num, term_code)

            COURSE_DEFAULTS = {
                'term_code': term_code,
                'name': section_name.title(),
                'dept': dept,
                'course_num': course_num,
                'least_credits': least_credits,
                'most_credits': most_credits,
                'description': None,
                'division_of_hours': None,
                'prereqs': 'None listed. Check Howdy.'
            }
            try:
                (course, created) = Course.objects.get_or_create(
                    _id=course_id, defaults=COURSE_DEFAULTS)
            except Exception as e:
                print(COURSE_DEFAULTS)
                print(dept)
                raise e

            SECTION_DEFAULTS = {
                '_id': _id,
                'term_code': term_code,
                'dept': dept,
                'course_num': course_num,
                'crn': crn,
                'section_num': section_num,
                'honors': honors,
                'section_name': section_name,
                'course': course,
                'least_credits': least_credits,
                'most_credits': most_credits
            }
            (s, created) = Section.objects.update_or_create(term_code=term_code, crn=crn,
                                                            defaults=SECTION_DEFAULTS)
            if meetings:
                s.meetings.set(meetings, clear=True)
    except requests.exceptions.ConnectionError as e:
        # Currently, this seems to be the only way
        # to get around TAMU's ECONNRESETs. A better
        # way would make a great PR.
        print('ECONNRESET in %s' % dept)
        collect(dept, int(term_code))


for term_code in request_term_codes():
    for dept in request_depts(term_code):
        collect(dept, int(term_code))
        print(term_code, '-', dept)
