import os
import sys
from datetime import datetime
from pprint import pprint

import django
import PyPDF2
import requests
from bs4 import BeautifulSoup

sys.path.append(
    os.path.realpath(
        os.path.join(
            os.path.dirname(__file__),
            '../server/')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

from goodbullapi.models import Section, GPADistribution

LEN_HEADER_ROW = 38

LEN_SECTION_ROW = 20
LEN_COURSE_TOTAL_ROW = 19
LEN_COLLEGE_TOTAL_ROW = 19
LEN_DEPT_TOTAL_ROW = 19

PDF_DOWNLOAD_DIR = 'pdfs/'


def download_pdf(url):
    local_filename = url.split('/')[-1]
    download_path = PDF_DOWNLOAD_DIR + local_filename
    try:
        r = requests.get(url)
        with open(download_path, 'wb+') as f:
            f.write(r.content)
        return download_path
    except requests.exceptions.HTTPError as e:
        print('404 on ' + url)


def is_header_row(text):
    return text == 'SECTION'


def is_course_total_row(text):
    return text == 'COURSE TOTAL:'


def is_college_total_row(text):
    return text == 'COLLEGE TOTAL:'


def is_dept_total_row(text):
    return text == 'DEPARTMENT TOTAL:'


def open_pdf(path):
    try:
        return PyPDF2.PdfFileReader(open(path, 'rb'))
    except PyPDF2.utils.PdfReadError:
        print("Tried to open invalid PDF. This is expected behavior, due to inconsistencies in TAMU data. Skipping this PDF.")


def extract_page_data(page_text):
    # Split the contents of the page on newlines, and strip whitespace from entries
    page_text = page_text.split('\n')
    page_text = [elem.strip() for elem in page_text]
    i = 0
    while i < len(page_text):
        if is_header_row(page_text[i]):
            i += LEN_HEADER_ROW
        elif is_course_total_row(page_text[i]):
            i += LEN_COURSE_TOTAL_ROW
        elif is_college_total_row(page_text[i]):
            i += LEN_COLLEGE_TOTAL_ROW
        elif is_dept_total_row(page_text[i]):
            i += LEN_DEPT_TOTAL_ROW
        else:
            section_row = page_text[i:i+LEN_SECTION_ROW]
            try:
                dept, course, section_num = section_row[0].split('-')
                instructor = section_row[-1]
                ABCDFQ = section_row[1:10:2]
                ABCDFQ.append(section_row[16])
                ABCDFQ = [int(letter_grade) for letter_grade in ABCDFQ]
                yield ((dept, course, section_num), instructor, ABCDFQ)
                i += LEN_SECTION_ROW
            except ValueError as e:
                # For some reason, A&M thought it was a good idea
                # to include sections that had TBA professors all semester?
                # Dunno why this is, but there's a missing entry at the
                # end of some rows. Just move to the next row.
                # How would we correlate the professor an
                i += LEN_SECTION_ROW - 1


def extract_pdf_data(pdf_reader):
    for i in range(pdf_reader.getNumPages()):
        current_page = pdf_reader.getPage(i)
        current_page_text = current_page.extractText()
        current_page_text = current_page_text.strip()
        for section in extract_page_data(current_page_text):
            yield section


def abbreviations():
    ROOT_URL = 'http://web-as.tamu.edu/gradereport/'
    r = requests.get(ROOT_URL)
    soup = BeautifulSoup(r.text, 'lxml')
    abbreviations = [elem['value'] for elem in soup.select(
        '#ctl00_plcMain_lstGradCollege > option')]
    # Ignore all "PROF" options, those are for professional school
    abbreviations = [elem for elem in abbreviations if 'PROF' not in elem]
    # Ignore the UT option, that's for University Totals
    return abbreviations[:-1]


def terms():
    SPRING = '1'
    SUMMER = '2'
    FALL = '3'
    SEMESTERS = [SPRING, SUMMER, FALL]
    YEARS = map(str, range(2017, datetime.now().year))
    for year in YEARS:
        for semester in SEMESTERS:
            yield year + semester


def urls():
    TEMPLATE_URL = 'http://web-as.tamu.edu/gradereport/PDFReports/%s/grd%s%s.pdf'
    for term in terms():
        for abbr in abbreviations():
            yield TEMPLATE_URL % (term, term, abbr)


if __name__ == '__main__':
    SPECIAL_CASES = {'GV': '2', 'QT': '3'}
    for url in urls():
        pprint(url)
        download_path = download_pdf(url)
        term = url[-11:-6]
        abbr = url[-6:-4]
        if download_path:
            pdf_reader = open_pdf(download_path)
            if pdf_reader:
                for section_gpa_data in extract_pdf_data(pdf_reader):
                    (dept, course_num, section_num), instructor, ABCDFQ = section_gpa_data
                    pprint(section_gpa_data)
                    #'1' = College Station, '2' = Galveston, '3' = Qatar
                    campus = '1' if abbr not in SPECIAL_CASES else SPECIAL_CASES[abbr]
                    term_code = int(term + campus)
                    section = None
                    try:
                        section = Section.objects.get(
                        term_code=term_code, dept=dept, course_num=course_num, section_num=section_num)
                    except Section.DoesNotExist:
                        print('Section not found for ' + str(section_gpa_data))
                    if section:
                        (g, created) = GPADistribution.objects.update_or_create(section=section, ABCDFQ=ABCDFQ)
