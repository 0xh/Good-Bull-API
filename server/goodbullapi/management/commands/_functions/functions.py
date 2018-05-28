import codecs
import csv
import re
import urllib
from pprint import pprint

import requests
from bs4 import BeautifulSoup, NavigableString


def stream_csv(url):
    """
    Generator function.
    Given a URL, makes a request to that URL,
    and yield each non-header row of the CSV.
    """
    file_stream = urllib.request.urlopen(url)
    csvfile = csv.reader(codecs.iterdecode(file_stream, 'utf-8'))
    next(csvfile)
    for row in csvfile:
        yield row


def request_html(url, headers=None):
    """
    Given a URL, makes a request to that
    URL, and returns the HTML.
    """
    r = requests.get(url)
    r.raise_for_status()
    return r.text


def request_catalog_departments(level):
    """
    Given an education level, returns a list of abbreviations and links
    to all of the courses offered at that education level.
    """
    assert level in ['undergraduate', 'graduate']

    ROOT_URL = 'http://catalog.tamu.edu'
    CATALOG_URL = ROOT_URL + '/{education_level}/course-descriptions/'

    url = CATALOG_URL.format(education_level=level)
    html = request_html(url)
    soup = BeautifulSoup(html, 'lxml')
    dept_a_elements = soup.select('#atozindex > ul > li > a')

    for elem in dept_a_elements:
        abbr = elem.get_text()[:4]
        href = elem.attrs['href']
        yield (abbr, ROOT_URL + href,)


def sanitize(text):
    """
    Removes non-breaking spaces for regular expression matching.
    """
    text = text.replace(u'\xa0', u' ')
    text = re.sub('\n+', ' ', text)
    text = re.sub(' +', ' ', text)
    text = text.strip()
    return text


def parse_title(course_block_title_text):
    try:
        COURSENUM_TITLE_PATTERN = r'[a-zA-Z]{3,4} (?P<course_num>[0-9]{3,4}[a-zA-Z]?)\/?(?:[a-zA-Z]{4} [0-9]{3,4}[a-zA-Z]?)? (?P<name>.+)'
        # For clarity, this pattern selects the sequences in [] from the examples below:
        # AALO [285] [Directed Studies]
        # EXAM [123S]/EXAM 789 [Cross-listed example 1]
        # EXAM [1234]/EXAM 123S [Cross-listed example 2]
        # LAW [123]/EXAM 123S [Cross-listed example 3]
        # LAW [7600]/EXAM 1234 [Cross-listed example 4]
        # ACCT [430]/IBUS 428 [Global Immersion in Accounting]

        course_num, name = re.findall(
            COURSENUM_TITLE_PATTERN, course_block_title_text)[0]
        return course_num, name
    except Exception as e:
        print(repr(course_block_title_text))
        return None


def parse_credits(credits_text):
    VARYING_CREDITS_PATTERN = re.compile(
        'Credits (?P<minimum_credits>[0-9]+) (?:to|or) (?P<maximum_credits>[0-9]+).')
    # For clarity, this pattern selects the sequences in [] from the examples below:
    # Credits [1] to [4].
    # Credits [1] or [4].
    # Credits [1] to [4].
    # Credits [1] to [4].

    CONCRETE_CREDITS_PATTERN = re.compile('Credits? (?P<credits>[0-9]+)')
    # For clarity, this pattern selects the sequences in [] from the examples below:
    # Credit [1].
    # Credits [4].

    matches = re.findall(VARYING_CREDITS_PATTERN, credits_text)
    min_credits = max_credits = None
    if matches:
        min_credits, max_credits = matches[0]
    else:
        matches = re.findall(CONCRETE_CREDITS_PATTERN, credits_text)
        min_credits = max_credits = matches[0]
    return int(min_credits), int(max_credits)


def split_into_reqs_and_desc(text):
    """
    Splits the provided course block description into
    its description, prerequisites, and corequisites.
    """
    PREREQ_COREQ_PATTERN = re.compile(
        ' Prerequisites?: | Corequisites?: | Cross Listing: ')
    split_text = re.split(PREREQ_COREQ_PATTERN, text)
    description = prereqs = coreqs = None
    if len(split_text) == 1:
        description = split_text[0]
    elif len(split_text) == 2:
        # Description and prerequisites only
        description, prereqs = split_text
    elif len(split_text) == 3:
        if 'Cross Listing' in text:
            description, prereqs, cross_listing = split_text
        else:
            description, prereqs, coreqs = split_text
    elif len(split_text) == 4:
        description, prereqs, cross_listing, coreqs = split_text
    return description, prereqs, coreqs


def get_element_text(soup, css_tag):
    """
    Given a BeautifulSoup object and a CSS selector,
    returns the sanitized (whitespace and non-breaking spaces removed)
    text contained in that element.
    """
    text = soup.select_one(css_tag).get_text()
    return sanitize(text)


def parse_course_block(course_block):
    course_block_title_text = get_element_text(
        course_block, '.courseblocktitle')
    course_num = title = None
    results = parse_title(
        course_block_title_text)
    if not results:
        return None
    course_num, title = results
    hours_text = get_element_text(course_block, '.hours')
    credits, distribution_of_hours = hours_text.split('.', 1)
    min_credits, max_credits = parse_credits(credits)

    course_block_desc = get_element_text(course_block, '.courseblockdesc')
    description, prereqs, coreqs = split_into_reqs_and_desc(
        course_block_desc)

    return course_num, title, min_credits, max_credits, distribution_of_hours, description, prereqs, coreqs


def request_catalog_instructors():
    """
    Searches the graduate and undergraduate faculty lists,
    and returns all of the (lastname, firstname) pairs 
    of each faculty listed.
    """
    FACULTY_URL = 'http://catalog.tamu.edu/{education_level}/faculty'
    UNDERGRADUATE = 'undergraduate'
    GRADUATE = 'graduate'
    education_levels = [UNDERGRADUATE, GRADUATE]
    for edu_lvl in education_levels:
        url = FACULTY_URL.format(education_level=edu_lvl)
        html = request_html(url)
        soup = BeautifulSoup(html, 'lxml')
        instructor_blocks = soup.select('.keeptogether > p')
        for instructor_block in instructor_blocks:
            # Generates empty string at beginning (for opening p)
            # and newline, empty string at end (for last br, and closing p)
            # Name is always located in the 1st position (not 0th)
            name = re.split(r'<p>|<br/>|</p>', str(instructor_block))[1]
            # The format of their name is "lastname, firstname"
            lastname, firstname = name.split(', ')[:2]
            yield lastname, firstname


def request_compass_depts(term_code):
    """
    Given a term code, requests all of the departments
    offering courses during that term.
    """
    URL = 'https://compass-ssb.tamu.edu/pls/PROD/bwckgens.p_proc_term_date'
    FORM_DATA = {
        'p_calling_proc': 'bwckschd.p_disp_dyn_sched',
        'p_term': term_code
    }
    response = requests.post(URL, FORM_DATA)
    soup = BeautifulSoup(response.text, 'html.parser')
    options = soup.find(id='subj_id').find_all('option')
    for option in options:
        yield option['value']


def is_professional_term(term_code):
    return term_code[4] == '4'


def is_half_year_term(term_code):
    return term_code[-1] == '5'


def is_term_of_interest(term_code):
    """
    Wrapper function to ensure that the term is neither
    a professional term (irrelevant to most students)
    nor a half-year term (not even sure what that is)
    """
    return not is_half_year_term(term_code) and not is_professional_term(term_code)


def request_compass_term_codes(full_scrape=False):
    """
    Retrieves all of the term codes of the compass section catalog.
    Takes one argument, `full_scrape` (Boolean)
    - True: Scrape every term code available (time-consuming, should only be done once every month or so)
    - False: Scrape the first twelve terms (quick, used for frequent updating)
    """
    URL = 'https://compass-ssb.tamu.edu/pls/PROD/bwckschd.p_disp_dyn_sched'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
    }
    html = request_html(URL, headers=HEADERS)
    soup = BeautifulSoup(html, 'lxml')
    options = soup.find_all('option', {'value': True})

    # Using slice notation
    LAST_TERM_TO_SCRAPE = -35
    SHALLOW_SCRAPE_CUTOFF = 12
    CURRENT_TERM = 1

    if not full_scrape:
        LAST_TERM_TO_SCRAPE = SHALLOW_SCRAPE_CUTOFF

    for option in options[CURRENT_TERM:LAST_TERM_TO_SCRAPE]:
        if is_term_of_interest(option['value']):
            yield option['value']


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


def request_compass_sections(dept, term_code):
    """
    Provided a department and term code,
    scrapes all of the sections for that department
    during that term.
    """
    URL = 'https://compass-ssb.tamu.edu/pls/PROD/bwckschd.p_get_crse_unsec?term_in={}&sel_subj=dummy&sel_day=dummy&sel_schd=dummy&sel_insm=dummy&sel_camp=dummy&sel_levl=dummy&sel_sess=dummy&sel_instr=dummy&sel_ptrm=dummy&sel_attr=dummy&sel_subj={}&sel_crse=&sel_title=&sel_schd=%25&sel_insm=%25&sel_from_cred=&sel_to_cred=&sel_camp=%25&sel_levl=%25&sel_ptrm=%25&sel_instr=%25&sel_attr=%25&begin_hh=0&begin_mi=0&begin_ap=a&end_hh=0&end_mi=0&end_ap=a'.format(
        term_code,
        dept)
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
    }
    html = request_html(URL, headers=HEADERS)
    soup = BeautifulSoup(html, 'lxml')
    outer_datadisplaytable = soup.select_one('table.datadisplaytable')
    section_elements = merge_trs(outer_datadisplaytable)
    pprint(section_elements)
