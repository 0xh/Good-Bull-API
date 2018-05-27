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


def parse_title(course_block_title_text):
    COURSENUM_TITLE_PATTERN = re.compile(
        '[a-zA-Z]{3,4} (?P<course_num>[0-9]{3,4}[a-zA-Z]{0,1})\/{0,1}(?:[a-zA-Z]{4} [0-9]{3,4}[a-zA-Z]{0,1}){0,1} (?P<name>.+)')
    # For clarity, this pattern selects the sequences in [] from the examples below:
    # AALO [285] [Directed Studies]
    # EXAM [123S]/EXAM 789 [Cross-listed example 1]
    # EXAM [1234]/EXAM 123S [Cross-listed example 2]
    # LAW [123]/EXAM 123S [Cross-listed example 3]
    # LAW [7600]/EXAM 1234 [Cross-listed example 4]
    # ACCT [430]/IBUS 428 [Global Immersion in Accounting]
    return re.findall(
        COURSENUM_TITLE_PATTERN, course_block_title_text)[0]
