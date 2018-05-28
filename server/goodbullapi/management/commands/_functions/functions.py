import codecs
import csv
import re
import urllib
from pprint import pprint

import requests

from bs4 import BeautifulSoup


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


def request_html(url):
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
