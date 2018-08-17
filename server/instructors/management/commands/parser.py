import datetime

import requests
import bs4
import PyPDF2
from typing import NewType, List, Dict, Tuple
import re
A = B = C = D = F = I = S = U = Q = X = int
Dept = CourseNum = SectionNum = str
GradeData = NewType(
    'NewType', Tuple[A, B, C, D, F, I, S, U, Q, X, Dept, CourseNum, SectionNum])


def generate_term_codes():
    """Generator function. Generates term codes.

    Yields:
        YEAR + SEMESTER CODE
    """
    year = datetime.datetime.now().year
    SPRING, SUMMER, FALL = 1, 2, 3
    while (year >= 2013):
        for semester in (SPRING, SUMMER, FALL):
            yield (str(year) + str(semester))
        year -= 1


def parse_page(page_obj: PyPDF2.pdf.PageObject) -> List[GradeData]:
    text = page_obj.extractText()
    text = re.split(r'\n+', text)
    text = [t.strip() for t in text]
    print(text)
    return []


def parse_pdf(pdf_reader: PyPDF2.PdfFileReader) -> List[GradeData]:
    pdf_data = []
    for i in range(pdf_reader.getNumPages()):
        page_data = parse_page(pdf_reader.getPage(i))
        pdf_data += page_data
    return pdf_data
