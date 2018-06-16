import collections
import re
from datetime import datetime
from pprint import pprint as print
from typing import List

import bs4
from django.core.management.base import BaseCommand
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from django.db.models import F

import goodbullapi.management.commands._common_functions as common_functions
from goodbullapi.models import Building, Instructor

HEADERS = {}


def request_term_codes():
    """Makes a request to TERM_CODE_URL to retrieve all the term codes.
    
    Returns:
        A list of all the term codes available.
    """
    TERM_CODE_URL = 'https://compass-ssb.tamu.edu/pls/PROD/bwckschd.p_disp_dyn_sched'
    soup = common_functions.request_html(TERM_CODE_URL)
    options = soup.select('select[name=p_term] > option')
    return [option['value'] for option in options]


def request_depts(term_code: int) -> List:
    """Makes a request to the DEPT_LIST_URL to retrieve all depts.

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
    soup = common_functions.request_html(
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
    return common_functions.request_html(URL, headers=HEADERS)


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


def parse_ddtitle(ddtitle):
    """Extracts the abbreviated name, CRN, and section number from the ddtitle.

    Args:
        ddtitle: A bs4.BeautifulSoup instance
    Returns:
        name: The abbreviated name of the section (used if course doesn't exist)
        CRN: The unique Course Registration Number that identifies this section within a term.
        section_num: The section number that, when combined with a department and course number, uniquely identifies this section.
    """
    title_text = ddtitle.select_one('a').text
    title_text = common_functions.sanitize(title_text)
    split_text = title_text.split(' - ')
    section_num = split_text[-1]
    crn = int(split_text[-3])
    _, course_num = split_text[-2].split(' ')

    name = ' '.join(split_text[0:-3])
    return name, crn, course_num, section_num


def parse_hours(dddefault: bs4.BeautifulSoup):
    """Extacts the number of hours from dddefault

    Args:
        dddefault: A bs4.BeautifulSoup instance
    Returns:
        min_hours: The minimum number of hours that this section can be worth
        max_hours: The maximum number of hours that this section can be worth
    """
    HOURS_PATTERN = re.compile(
        '(?:([\d\.]+)(?:\s+TO\s+|\s+OR\s+))?([\d\.]+)\s+Credits?')
    try:
        min_hours, max_hours = re.findall(HOURS_PATTERN, dddefault.text)[0]
        max_hours = float(max_hours)
        if not min_hours:
            min_hours = max_hours
        else:
            min_hours = float(min_hours)
        return min_hours, max_hours
    except Exception as e:
        print(dddefault.text)
        raise e


def is_tba(string):
    return string.strip() == "TBA"


def parse_duration(duration_string):
    """Parse and calculate the duration of a meeting.

    Args:
        duration_string: A string matching format %I:%M %p (see Python docs on datetime)
    Returns:
        A datetime.timedelta representing the duration of this meeting time, or None if TBA.
    """
    TIME_FORMAT_STRING = '%I:%M %p'
    if is_tba(duration_string):
        return None
    start_string, end_string = duration_string.upper().split(' - ')
    start_string = start_string.strip()
    start_time = datetime.strptime(start_string, TIME_FORMAT_STRING)

    end_string = end_string.strip()
    end_time = datetime.strptime(end_string, TIME_FORMAT_STRING)
    return end_time - start_time


def has_primary_mark(instructor):
    return '(P)' in instructor


def strip_primary_mark(instructor):
    return instructor.replace('(P)', '')


def reduce_whitespace(string):
    return re.sub('\s+', ' ', string)


def retrieve_building(location: str):
    """Searches Building database for instance with name most similar to location (if not TBA).

    Args:
        location: The string to search on.
    Returns:
        The closest matching building instance (if not TBA, else None)
    """
    # TODO: SearchRanking removes stopwords
    if is_tba(location):
        return None
    location = location.split(' ')[0]
    query = SearchQuery(location.lower())
    qset = Building.objects.annotate(rank=SearchRank(
        F('search_vector'), query)).order_by('-rank').values_list('abbr', flat=True)
    print(qset)
    return None

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
            if has_primary_mark(instructor):
                instructor = strip_primary_mark(instructor)
                primary_instructor_name = reduce_whitespace(instructor)
    if not primary_instructor_name:
        cnt = collections.Counter(all_mentioned_instructors)
        primary_instructor_name = cnt.most_common(1)[0]
    instructor = Instructor.objects.get_or_create(name=primary_instructor_name)
    return instructor


def parse_meetings_and_retrieve_instructor(dddefault: bs4.BeautifulSoup):
    """Retieves all of the meetings that this class will be holding. Additionally, determines the instructor.

    Args:
        dddefault: A bs4.BeautifulSoup instance
    Returns:
        A list of Meeting instances, and either an instructor instance or None
    """
    datadisplaytable = dddefault.select_one('.datadisplaytable')
    # Because TAMU doesn't know what `th` elements are, throw out the first row.
    rows = datadisplaytable.select('tr')[1:]

    all_mentioned_instructors = []
    meetings = []
    for row in rows:
        entries = [td.text.replace(u'\xa0', '') for td in row.select('td')]
        print(entries)
        meet_type, duration_string, days, location, _, _, instructor_string = entries
        duration = parse_duration(duration_string)
        building = retrieve_building(location)
        all_mentioned_instructors.append(instructor_string)

    instructor, _ = retrieve_instructor(all_mentioned_instructors)
    return meetings, instructor


def parse_dddefault(dddefault: bs4.BeautifulSoup):
    """Extracts the number of hours and the meetings from a dddefault element.

    Args:
        dddefault: A dddefault element that contains hours and meeting data.
    Returns:
        min_hours: The minimum number of hours that this section can be worth.
        max_hours: The minimum number of hours that this section can be worth.
        meetings: A list of Meeting instances.
    """
    min_hours, max_hours = parse_hours(dddefault)
    parse_meetings_and_retrieve_instructor(dddefault)
    return min_hours, max_hours


def extract_tr_data(tr):
    """Extract section data from tr.

    Args:
        tr: A bs4.BeautifulSoup instance
    Returns:
        name: The abbreviated name of the section (used if the course doesn't exist)
        CRN: The unique Course Registration Number that identifies this section within a term.
        section_num: The section number that, when combined with a department and course number, uniquely identifies this section.
    """
    ddtitle = tr.select_one('.ddtitle')
    name, crn, course_num, section_num = parse_ddtitle(ddtitle)
    dddefault = tr.select_one('.dddefault')
    min_hours, max_hours = parse_dddefault(dddefault)
    return name, crn, course_num, section_num, min_hours, max_hours


class Command(BaseCommand):
    help = 'Retrieves all of the sections in the Texas A&M University system'

    def handle(self, *args, **options):
        term_codes = request_term_codes()[1:]
        for term_code in term_codes[:1]:
            depts = request_depts(term_code)
            for dept in depts:
                print(dept)
                soup = request_dept_sections(term_code, dept)
                outer_datadisplaytable = soup.select_one(
                    'table.datadisplaytable')
                trs = merge_trs(outer_datadisplaytable)
                for tr in trs:
                    print(extract_tr_data(tr))
