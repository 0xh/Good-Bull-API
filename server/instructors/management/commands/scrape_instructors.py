import os

import bs4
import PyPDF2
import requests
from django.core.management import base as mgmt_base

from instructors.management.commands import parser

PDF_URL = 'http://web-as.tamu.edu/gradereport/PDFReports/%s/grd%s%s.pdf'
PDF_DIR = os.path.abspath('server/instructors/management/commands/pdfs')


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
    options = [o['value'] for o in options]
    return options


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


class Command(mgmt_base.BaseCommand):
    def handle(self, *args, **options):
        abbreviations = get_college_abbreviations()
        for term_code in parser.generate_term_codes():
            print(term_code)
            for abbr in abbreviations:
                print(abbr)
                pdf_path = download_pdf(
                    PDF_URL % (term_code, term_code, abbr))
                if pdf_path is None:
                    continue
                with open(pdf_path, 'rb') as f:
                    pdf_reader = PyPDF2.PdfFileReader(f)
                    grade_distributions = parser.parse_pdf(pdf_reader)
                    print(grade_distributions)
