import PyPDF2
from pprint import pprint

LEN_TITLE_ROW = 38
LEN_COURSE_TOTAL_ROW = LEN_DEPT_TOTAL_ROW = 19
LEN_SECTION_ROW = LEN_COLLEGE_TOTAL_ROW = 20

INSTRUCTORS = {}

SEMESTERS = ['Fall', 'Spring', 'Summer']

def is_title_row(elem):
    return elem == 'SECTION'


def is_course_total_row(elem):
    return elem == 'COURSE TOTAL:'


def is_dept_total_row(elem):
    return elem == 'DEPARTMENT TOTAL:'


def is_college_total_row(elem):
    return elem == 'COLLEGE TOTAL:'


def is_empty_row(elem):
    """
    Inaccuracies in reading the PDF cause these 
    empty rows to appear every once in a while.
    """
    return elem == ''


def extract_section_data(section_row):
    section_id = tuple(section_row[0].split('-'))
    instructor_id = section_row[-1]
    ABCDFQ = [int(x) for x in section_row[1:10:2]]
    ABCDFQ.append(int(section_row[-4]))
    return section_id, instructor_id, ABCDFQ


def extract_page_data(page_text):
    """
    Retrieves all of the relevant information regarding
    sections on each page (instructors, grade distributions, section id)
    """
    i = 0
    page_data = []
    while i < len(page_text):
        if is_title_row(page_text[i]):
            i += LEN_TITLE_ROW
        elif is_course_total_row(page_text[i]):
            i += LEN_COURSE_TOTAL_ROW
        elif is_dept_total_row(page_text[i]):
            i += LEN_DEPT_TOTAL_ROW
        elif is_college_total_row(page_text[i]):
            i += LEN_COLLEGE_TOTAL_ROW
        else:
            section_row = page_text[i:i+LEN_SECTION_ROW]
            if is_empty_row(section_row[0]):
                break
            page_data.append(extract_section_data(section_row))
            i += LEN_SECTION_ROW
    return page_data


def extract_college_data(file_name):
    semester_id = file_name[3:8]
    year, semester = SEMESTERS[int(semester_id[-1])-1], semester_id[:-1]
    print(year, semester)
    pdf_file = open(file_name, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)
    college_sections = []
    for i in range(pdf_reader.getNumPages()):
        page_obj = pdf_reader.getPage(i)
        page_text = [elem.strip()
                     for elem in page_obj.extractText().split('\n')]
        college_sections += extract_page_data(page_text)
    return college_sections


college_sections = extract_college_data('grd20172AG.pdf')

