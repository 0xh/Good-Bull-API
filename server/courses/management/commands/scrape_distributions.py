import os
from typing import List

import bs4
import PyPDF2
import requests
from django.core import exceptions as django_exceptions
from django.core.management import base as mgmt_base

from courses import models as course_models
from courses.management.commands.parsers import pdf_parser

PDF_URL = 'http://web-as.tamu.edu/gradereport/PDFReports/%s/grd%s%s.pdf'
PDF_DIR = os.path.abspath('server/sections/management/commands/pdfs')


def get_college_abbreviations():
    """Makes a GET request to 'web-as.tamu.edu' to retrieve college
    abbreviations.

    Returns:
        A list of the college abbreviations.
    """
    r = requests.get('http://web-as.tamu.edu/gradereport/')
    r.raise_for_status()
    soup = bs4.BeautifulSoup(r.content, 'lxml')
    options = soup.select('#ctl00_plcMain_lstGradCollege > option')
    options = [o['value'] for o in options if 'PROF' not in o['value']]
    return options[:-1]


def download_pdf(url) -> str:
    """Downloads a PDF from a URL.

    Args:
        url: A URL indicating what PDF file to download.
    Returns:
        A path to the downloaded PDF file.
    """
    filename = url.split('/')[-1]
    path = os.path.join(PDF_DIR, filename)

    r = requests.get(url)
    try:
        r.raise_for_status()
        with open(path, 'wb+') as f:
            f.write(r.content)
            return path
    except requests.exceptions.HTTPError as e:
        if e.response.status_code != 404:
            raise e


def build_grade_distribution(letter_grades: List[int], gpa: float, section: course_models.Section) -> course_models.GradeDistribution:
    """Creates (or retrieves) a GradeDistribution instance.

    Args:
        letter_grades: The letter grades of the section
        gpa: The gpa of the section
        section: The related section
    """
    grade_distribution, _ = course_models.GradeDistribution.objects.get_or_create(
        section=section, ABCDFISUQX=letter_grades, gpa=gpa)
    return grade_distribution


def build_term_code(year_semester: str, abbr: str) -> int:
    """Creates a term_code from a year + semester string and an abbreviation.

    Args:
        year_semester: A string in the format "YYYYS" where Y=year and S is in {1, 2, 3}
        abbr: A short code indicating what college is being parsed.
    Returns:
        A 6-digit integer whose digits are: YYYYSU where U is in {1, 2, 3}
    """
    if abbr != 'GV' and abbr != 'QT':
        return int(year_semester + '1')
    else:
        if abbr == 'GV':
            return int(year_semester + '2')
        else:
            return int(year_semester + '3')


class Command(mgmt_base.BaseCommand):
    def handle(self, *args, **options):
        abbreviations = get_college_abbreviations()
        for year_semester in pdf_parser.generate_year_semesters():
            print(year_semester)
            for abbr in abbreviations:
                print(abbr)
                term_code = build_term_code(year_semester, abbr)
                pdf_path = download_pdf(
                    PDF_URL % (year_semester, year_semester, abbr))
                if pdf_path is None:
                    continue
                with open(pdf_path, 'rb') as f:
                    pdf_reader = PyPDF2.PdfFileReader(f)
                    grade_distributions = pdf_parser.parse_pdf(pdf_reader)
                    for letter_grades, (dept, course_num, section_num), gpa in grade_distributions:
                        try:
                            course = course_models.Course.objects.get(
                                dept=dept, course_num=course_num)
                            section = course_models.Section.objects.get(
                                course=course, section_num=section_num, term_code=term_code)
                            grade_distribution = build_grade_distribution(
                                letter_grades, gpa, section)
                            section.grade_distribution = grade_distribution
                            section.save()
                        except django_exceptions.ObjectDoesNotExist:
                            continue
