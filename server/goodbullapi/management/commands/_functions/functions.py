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

    Positional arguments:
    - url -- the url to make a GET request to

    Keyword arguments:
    - headers -- optional headers to send alongside the GET request. (default None)
    """
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.text


def sanitize(string):
    """
    Given a string, removes duplicate whitespace and non-breaking characters.

    Positional arguments:
    - string -- the string to sanitize.
    """
    string = ''.join([i if ord(i) < 128 else ' ' for i in string])
    string = re.sub('\s+', ' ', string)
    return string.strip()


def parse_name(course_block_title_text):
    """
    Given a string which represents a title on https://catalog.tamu.edu, extracts the course number and the name of the course.

    Positional arguments:
    - course_block_title_text -- the course block's title text (which is the department, course number, any cross-listed courses, and the name of the course.)
    """
    COURSENUM_TITLE_PATTERN = r'[a-zA-Z]{3,4} (?P<course_num>[0-9]{3,4}[a-zA-Z]?)\/?(?:[a-zA-Z]{4} [0-9]{3,4}[a-zA-Z]?)? (?P<name>.+)'
    # For clarity, this pattern selects the sequences in [] from the examples below:
    # AALO [285] [Directed Studies]
    # EXAM [123S]/EXAM 789 [Cross-listed example 1]
    # EXAM [1234]/EXAM 123S [Cross-listed example 2]
    # LAW [123]/EXAM 123S [Cross-listed example 3]
    # LAW [7600]/EXAM 1234 [Cross-listed example 4]
    # ACCT [430]/IBUS 428 [Global Immersion in Accounting]
    course_block_title_text = sanitize(course_block_title_text)
    try:
        course_num, name = re.findall(
            COURSENUM_TITLE_PATTERN, course_block_title_text)[0]
        return course_num, name
    except Exception:
        print(repr(course_block_title_text))
        return None


def parse_credits(credits):
    """
    Given a string which represents the credits on https://catalog.tamu.edu, extracts the credits and the amount of time spent in each meeting type.

    Poitional arguments:
    - hours -- the course block's hour text (which contains the number of hours, and how long is spent in each meeting type)
    """
    hours = sanitize(credits)
    VARYING_CREDITS_PATTERN = re.compile(
        'Credits (?P<minimum_credits>[0-9]+) (?:to|or) (?P<maximum_credits>[0-9]+).')
    # For clarity, this pattern selects the sequences in [] from the examples below:
    # Credits [1] to [4].
    # Credits [1] or [4].

    CONCRETE_CREDITS_PATTERN = re.compile('Credits? (?P<credits>[0-9]+)')
    # For clarity, this pattern selects the sequences in [] from the examples below:
    # Credit [1].
    # Credits [4].

    matches = re.findall(VARYING_CREDITS_PATTERN, credits)
    min_credits = max_credits = None
    if matches:
        min_credits, max_credits = matches[0]
    else:
        matches = re.findall(CONCRETE_CREDITS_PATTERN, credits)
        min_credits = max_credits = matches[0]
    return int(min_credits), int(max_credits)


def parse_description(description_text):
    """
    Given a string which represents a title on https://catalog.tamu.edu, extracts the course number and the name of the course.

    Positional arguments:
    - description -- the course block's description text (which can include cross-listing, prerequisites, and corequisites)
    """
    PREREQ_COREQ_CROSSLIST_PATTERN = re.compile(
        ' Prerequisites?: | Corequisites?: | Cross Listing: ')
    description_text = sanitize(description_text)
    split_text = re.split(PREREQ_COREQ_CROSSLIST_PATTERN, description_text)
    description = prereqs = coreqs = None

    if len(split_text) == 1:
        description = split_text[0]
    elif len(split_text) == 2:
        # Includes description and prerequisites only.
        description, prereqs = split_text
    elif len(split_text) == 3:
        if 'Cross Listing' in description_text:
            description, prereqs, cross_listing = split_text
        else:
            description, prereqs, coreqs = split_text
    elif len(split_text) == 4:
        description, prereqs, cross_listing, coreqs = split_text
    return description, prereqs, coreqs


def request_catalog_depts(level):
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


def get_element_text(soup, css_tag):
    """
    Given a BeautifulSoup object and a CSS selector,
    returns the sanitized (whitespace and non-breaking spaces removed)
    text contained in that element.
    """
    text = soup.select_one(css_tag).get_text()
    return text


def parse_course_block(course_block):
    course_num = title = None
    course_block_title_text = get_element_text(
        course_block, '.courseblocktitle')
    results = parse_name(course_block_title_text)
    if not results:
        return None
    course_num, title = results
    hours_text = get_element_text(course_block, '.hours')
    credits, distribution_of_hours = hours_text.split('.', 1)
    min_credits, max_credits = parse_credits(credits)

    course_block_desc = get_element_text(course_block, '.courseblockdesc')
    description, prereqs, coreqs = parse_description(
        course_block_desc)
    return course_num, title, min_credits, max_credits, distribution_of_hours, description, prereqs, coreqs
