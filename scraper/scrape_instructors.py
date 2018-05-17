
from datetime import datetime
from pprint import pprint

import PyPDF2
import requests
from bs4 import BeautifulSoup

import sync_with_django_orm
from goodbullapi.models import GPADistribution, Section

LEN_HEADER_ROW = 38

LEN_SECTION_ROW = 20
LEN_COURSE_TOTAL_ROW = LEN_COLLEGE_TOTAL_ROW = LEN_DEPT_TOTAL_ROW = 19

PDF_DOWNLOAD_DIR = 'pdfs/'


def download_pdf(url):
    local_filename = url.split('/')[-1]
    download_path = PDF_DOWNLOAD_DIR + local_filename
    try:
        r = requests.get(url)
        with open(download_path, 'wb+') as f:
            f.write(r.content)
        return download_path
    except requests.exceptions.HTTPError:
        print('404 on ' + url)


def is_header_row(text):
    """
    Given a \"row\" in a grade distribution PDF, determines if the row is one that
    contains header information (such as what each column is, various formatting
    dashes, etc.)
    Used to skip rows.
    """
    return text == 'SECTION'


def is_course_total_row(text):
    """
    Given a \"row\" in a grade distribution PDF, determines if the row is one that 
    displays the number of letter grades distributed across an entire course.
    Used to skip rows.
    """
    return text == 'COURSE TOTAL:'


def is_college_total_row(text):
    """
    Given a \"row\" in a grade distribution PDF, determines if the row is one that 
    displays the number of letter grades distributed across the entire college.
    Used to skip rows.
    """
    return text == 'COLLEGE TOTAL:'


def is_dept_total_row(text):
    """
    Given a \"row\" in a grade distribution PDF, determines if the row is one that
    displays the number of letter grades distributed across an entire department.
    Used to skip rows.
    """
    return text == 'DEPARTMENT TOTAL:'


def open_pdf(path):
    """
    Creates a PyPDF2.PdfFileReader instance around the path provided. This
    function can throw an error, which is because the path provided doesn't lead to
    a valid PDF. This is expected behavior, TAMU is very inconsistent in their error
    handling methods.
    """
    try:
        return PyPDF2.PdfFileReader(open(path, 'rb'))
    except PyPDF2.utils.PdfReadError:
        print("Tried to open invalid PDF. This is expected behavior, due to inconsistencies in TAMU data. Skipping this PDF.")


def extract_page_data(page_text):
    """
    Retrieves the letter grade distributions (number of As, Bs, Cs, etc.) for all of the
    sections on this page.
    """
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
    """
    A generator function that yields the section data in a grade distribution PDF.
    """
    for i in range(pdf_reader.getNumPages()):
        current_page = pdf_reader.getPage(i)
        current_page_text = current_page.extractText()
        current_page_text = current_page_text.strip()
        for section in extract_page_data(current_page_text):
            yield section


def request_college_abbreviations():
    ROOT_URL = 'http://web-as.tamu.edu/gradereport/'
    r = requests.get(ROOT_URL)
    soup = BeautifulSoup(r.text, 'lxml')
    abbreviations = [elem['value'] for elem in soup.select(
        '#ctl00_plcMain_lstGradCollege > option')]
    # Ignore all "PROF" options, those are for professional school
    abbreviations = [elem for elem in abbreviations if 'PROF' not in elem]
    # Ignore the UT option, that's for University Totals
    return abbreviations[:-1]


def generate_terms():
    SPRING = '1'
    SUMMER = '2'
    FALL = '3'
    SEMESTERS = [SPRING, SUMMER, FALL]
    YEARS = map(str, range(datetime.now().year, 2013, -1))
    for year in YEARS:
        for semester in SEMESTERS:
            yield year + semester


def generate_urls():
    """
    Generates URLs to retrieve every grade distribution
    for every college for every term.
    """
    TEMPLATE_URL = 'http://web-as.tamu.edu/gradereport/PDFReports/%s/grd%s%s.pdf'
    for term in generate_terms():
        for abbr in request_college_abbreviations():
            yield TEMPLATE_URL % (term, term, abbr)


def calculate_gpa(ABCDFQ):
    A = 4.0
    B = 3.0
    C = 2.0
    D = 1.0
    F = 0.0
    WEIGHTS = [A, B, C, D, F]
    # Ignore students with extenuating circumstances
    # (I, W, F*, etc.)
    NUM_STUDENTS = sum(ABCDFQ)
    total_credits = 0
    for (students_with_this_grade, weight) in zip(ABCDFQ, WEIGHTS):
        total_credits += students_with_this_grade * weight
    return total_credits / NUM_STUDENTS


if __name__ == '__main__':

    for url in generate_urls():
        pprint(url)
        download_path = download_pdf(url)
        term = url[-11:-6]
        abbr = url[-6:-4]
        if download_path:
            pdf_reader = open_pdf(download_path)
            if pdf_reader:
                for section_gpa_data in extract_pdf_data(pdf_reader):
                    (dept, course_num, section_num), instructor, ABCDFQ = section_gpa_data

                    COLLEGE_STATION = '1'
                    GALVESTON = '2'
                    QATAR = '3'
                    SPECIAL_CASES = {'GV': GALVESTON, 'QT': QATAR}
                    campus = COLLEGE_STATION
                    if abbr in SPECIAL_CASES:
                        campus = SPECIAL_CASES[abbr]
                    term_code = int(term + campus)
                    section = None
                    try:
                        section = Section.objects.get(
                            term_code=term_code, dept=dept, course_num=course_num, section_num=section_num)
                    except Section.DoesNotExist:
                        print('Section not found for ' + str(section_gpa_data))
                    if section:
                        (g, created) = GPADistribution.objects.update_or_create(
                            section=section, ABCDFQ=ABCDFQ, gpa=calculate_gpa(ABCDFQ))
