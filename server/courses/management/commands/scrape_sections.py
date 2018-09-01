import collections
import re
from datetime import datetime
from pprint import pprint as print
from typing import List

import bs4
import requests
from django.core.management.base import BaseCommand
from django.db import transaction

from courses import models as course_models
from instructors import models as instructor_models
from courses import models as course_models
from courses.management.commands.parsers.howdy_parser import (body_functions,
                                                               title_functions)
from shared.functions import scraper_functions

HEADERS = {}


def request_term_codes():
    """Makes a request to retrieve all the term codes.
    
    Returns:
        A list of all the term codes available.
    """
    TERM_CODE_URL = 'https://compass-ssb.tamu.edu/pls/PROD/bwckschd.p_disp_dyn_sched'
    soup = scraper_functions.request_html(TERM_CODE_URL)
    options = soup.select('select[name=p_term] > option')
    return [option['value'] for option in options]


def request_depts(term_code: int) -> List:
    """Makes a request to retrieve all depts.

    Args:
        term_code: The term code for which to request depts.
    Returns:
        A list of department abbreviations.
    """
    DEPT_LIST_URL = 'https://compass-ssb.tamu.edu/pls/PROD/bwckgens.p_proc_term_date'
    FORM_DATA = {
        'p_calling_proc': 'bwckschd.p_disp_dyn_sched',
        'p_term': term_code
    }
    soup = scraper_functions.request_html(
        DEPT_LIST_URL, form_data=FORM_DATA, post=True)
    options = soup.select('select[name=sel_subj] > option')
    return [option['value'] for option in options]


def request_dept_sections(term_code: int, dept: str):
    """Makes a request to retrieve all the sections for a department for a term.

    Args:
        term_code: The term code for which to request departments.
        dept: The 3-to-4 letter dept abbreviation
    Returns:
        A BeautifulSoup instance.
    """
    URL = 'https://compass-ssb.tamu.edu/pls/PROD/bwckschd.p_get_crse_unsec?term_in={}&sel_subj=dummy&sel_day=dummy&sel_schd=dummy&sel_insm=dummy&sel_camp=dummy&sel_levl=dummy&sel_sess=dummy&sel_instr=dummy&sel_ptrm=dummy&sel_attr=dummy&sel_subj={}&sel_crse=&sel_title=&sel_schd=%25&sel_insm=%25&sel_from_cred=&sel_to_cred=&sel_camp=%25&sel_levl=%25&sel_ptrm=%25&sel_instr=%25&sel_attr=%25&begin_hh=0&begin_mi=0&begin_ap=a&end_hh=0&end_mi=0&end_ap=a'.format(
        int(term_code), dept)
    return scraper_functions.request_html(URL, headers=HEADERS)


def merge_trs(outer_datadisplaytable):
    """Poorly-designed HTML means TRs need to be merged.

    Args:
        outer_datadisplaytable: A bs4.BeautifulSoup instance
    Returns:
        A list of merged TRs.
    """
    trs = outer_datadisplaytable.contents[1:]
    trs = [tr for tr in trs if not isinstance(tr, bs4.NavigableString)]
    merged = []
    for tr in trs:
        if tr.select_one('th.ddtitle'):
            merged.append(tr)
        elif tr.select_one('td.dddefault'):
            merged[-1] = bs4.BeautifulSoup(str(merged[-1]) + str(tr), 'lxml')
    return merged


def retrieve_instructor(all_mentioned_instructors: List[str]):
    """Determines which of the instructors mentioned is the primary instructor.

    Args:
        all_mentioned_instructors: Sometimes there are multiple instructors assigned to a section.
    Returns:
        The primary instructor.
    """
    primary_instructor_name = None
    for instructors_mentioned in all_mentioned_instructors:
        instructors_mentioned = instructors_mentioned.split(',')
        for instructor in instructors_mentioned:
            if body_functions.has_primary_indicator(instructor):
                primary_instructor_name = instructor
                break
    if not primary_instructor_name:
        cnt = collections.Counter(all_mentioned_instructors)
        primary_instructor_name, _ = cnt.most_common(1)[0]
    if body_functions.is_tba(primary_instructor_name):
        return None
    primary_instructor_name = body_functions.strip_primary_indicator(
        primary_instructor_name)
    primary_instructor_name = reduce_whitespace(
        primary_instructor_name).strip()
    instructor, _ = instructor_models.Instructor.objects.get_or_create(
        name=primary_instructor_name)
    instructor.full_clean()
    return instructor


def reduce_whitespace(string):
    return re.sub(r'\s+', ' ', string)


def extract_tr_data(tr):
    """Extract section data from tr.

    Args:
        tr: A bs4.BeautifulSoup instance
    Returns:
        name: The abbreviated name of the section (used if the course doesn't exist)
        CRN: The unique Course Registration Number that identifies this section within a term.
        course_num: The course number that identifies the course that this section belongs to.
        section_num: The section number that, when combined with a department and course number, uniquely identifies this section.
        min_hours: The minimum number of hours that this section can count for.
        max_hours: The maximum number of hours that this section can count for.
        meetings: A list of Meeting instances.
        instructor: An Instructor instance (or none if the instructor is TBA)
    """
    ddtitle = tr.select_one('.ddtitle')
    name, crn, course_num, section_num = title_functions.parse_ddtitle(ddtitle)
    dddefault = tr.select_one('.dddefault')
    min_hours, max_hours, meeting_dicts, all_mentioned_instructors = body_functions.parse_dddefault(
        dddefault)
    meetings = []
    if meeting_dicts is not None:
        for meeting_dict in meeting_dicts:
            meeting = course_models.Meeting.objects.create(**meeting_dict)
            meetings.append(meeting)
    instructor = None
    if all_mentioned_instructors is not None:
        instructor = retrieve_instructor(all_mentioned_instructors)
    return name, crn, course_num, section_num, min_hours, max_hours, meetings, instructor


@transaction.atomic
def collect(dept: str, term_code: int):
    """Collects all of the sections offered by a department `dept` during `term_code`.

    Args:
        dept: The abbreviated department string.
        term_code: A term code indicating what term to look for.
    """
    print(dept)
    try:
        soup = request_dept_sections(term_code, dept)
        outer_datadisplaytable = soup.select_one('table.datadisplaytable')
        trs = merge_trs(outer_datadisplaytable)
        for tr in trs:
            name, crn, course_num, section_num, min_hours, max_hours, meetings, instructor = extract_tr_data(
                tr)
            # Get or create the related Course instance
            defaults = {
                '_id': dept + '-' + course_num,
                'dept': dept,
                'course_num': course_num,
                'name': name,
                'description': None,
                'min_credits': min_hours,
                'max_credits': max_hours,
            }
            course, _ = course_models.Course.objects.get_or_create(
                dept=dept, course_num=course_num, defaults=defaults)
            _id = str(crn) + '_' + str(term_code)
            section_defaults = {
                '_id': _id,
                'name': name,
                'crn': crn,
                'section_num': section_num,
                'term_code': term_code,
                'instructor': instructor,
                'course': course
            }
            section, _ = course_models.Section.objects.update_or_create(
                crn=crn, term_code=term_code, defaults=section_defaults)
            if meetings:
                section.meetings.set(meetings, clear=True)
    except requests.exceptions.ConnectionError as e:
        # To anybody reading this code in the future that's not me:
        # Do not do this to a website unless you're okay with hammering
        # it with a high number of requests.
        print('Connection error parsing %s-%i' % (dept, term_code))
        print(e)
        collect(dept, term_code)
    except ConnectionResetError:
        print('Connection reset error parsing %s-%i' % (dept, term_code))
        collect(dept, term_code)


class Command(BaseCommand):
    help = 'Retrieves all of the sections in the Texas A&M University system'

    def add_arguments(self, parser):
        parser.add_argument('--shallow', dest='shallow', action='store_true',
                            help='Parses only the first 8 term codes. Used for updating current terms.')

    def handle(self, *args, **options):
        term_codes = request_term_codes()[1:]
        if 'shallow' in options:
            term_codes = request_term_codes()[1:9]
        for term_code in term_codes:
            term_code = int(term_code)
            depts = request_depts(term_code)
            for dept in depts:
                collect(dept, term_code)
