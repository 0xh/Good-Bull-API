import goodbullapi.management.commands._common_functions as common_functions
from django.core.management.base import BaseCommand
from pprint import pprint as print
from goodbullapi.models import Building
from typing import List
import bs4

HEADERS = {}


def request_term_codes():
    """Makes a request to TERM_CODE_URL to retrieve all the term codes.
    
    Returns:
        A list of all the term codes available.
    """
    TERM_CODE_URL = 'https://compass-ssb.tamu.edu/pls/PROD/bwckschd.p_disp_dyn_sched'
    soup = common_functions.request_html(TERM_CODE_URL)
    options = soup.select('select[name=p_term] > option')
    return [option['value'] for option in options]


def request_depts(term_code: int) -> List:
    """Makes a request to the DEPT_LIST_URL to retrieve all depts.

    Args:
        term_code: The term code for which to request depts.
    Returns:
        A list of department abbreviations.
    """
    DEPT_LIST_URL = 'https://compass-ssb.tamu.edu/pls/PROD/bwckgens.p_proc_term_date'
    FORM_DATA = {
        'p_calling_proc': 'bwckschd.p_disp_dyn_sched',
        'p_term': term_code
    }
    soup = common_functions.request_html(
        DEPT_LIST_URL, form_data=FORM_DATA, post=True)
    options = soup.select('select[name=sel_subj] > option')
    return [option['value'] for option in options]


def request_dept_sections(term_code: int, dept: str):
    """Makes a request to retrieve all the sections for a department for a term.

    Args:
        term_code: The term code for which to request departments.
        dept: The 3-to-4 letter dept abbreviation
    Returns:
        A BeautifulSoup instance.
    """
    URL = 'https://compass-ssb.tamu.edu/pls/PROD/bwckschd.p_get_crse_unsec?term_in={}&sel_subj=dummy&sel_day=dummy&sel_schd=dummy&sel_insm=dummy&sel_camp=dummy&sel_levl=dummy&sel_sess=dummy&sel_instr=dummy&sel_ptrm=dummy&sel_attr=dummy&sel_subj={}&sel_crse=&sel_title=&sel_schd=%25&sel_insm=%25&sel_from_cred=&sel_to_cred=&sel_camp=%25&sel_levl=%25&sel_ptrm=%25&sel_instr=%25&sel_attr=%25&begin_hh=0&begin_mi=0&begin_ap=a&end_hh=0&end_mi=0&end_ap=a'.format(
        int(term_code), dept)
    return common_functions.request_html(URL, headers=HEADERS)


def merge_trs(outer_datadisplaytable):
    """Poorly-designed HTML means TRs need to be merged.

    Args:
        outer_datadisplaytable: A bs4.BeautifulSoup instance
    Returns:
        A list of merged TRs.
    """
    trs = outer_datadisplaytable.contents[1:]
    trs = [tr for tr in trs if not isinstance(tr, bs4.NavigableString)]
    merged = []
    for tr in trs:
        if tr.select_one('th.ddtitle'):
            merged.append(tr)
        elif tr.select_one('td.dddefault'):
            merged[-1] = bs4.BeautifulSoup(str(merged[-1]) + str(tr), 'lxml')
    return merged


def parse_ddtitle(ddtitle):
    """Extracts the abbreviated name, CRN, and section number from the ddtitle.

    Args:
        ddtitle: A bs4.BeautifulSoup instance
    Returns:
        name: The abbreviated name of the section (used if course doesn't exist)
        CRN: The unique Course Registration Number that identifies this section within a term.
        section_num: The section number that, when combined with a department and course number, uniquely identifies this section.
    """
    title_text = ddtitle.select_one('a').text
    title_text = common_functions.sanitize(title_text)
    split_text = title_text.split(' - ')
    section_num = split_text[-1]
    crn = int(split_text[-3])
    name = ' '.join(split_text[0:-3])
    return (name, crn, section_num)

def parse_dddefault(dddefault: bs4.BeautifulSoup):
    """Extracts the number of credits and the meetings from a dddefault element.

    Args:
        dddefault: A dddefault element that contains credits and meeting data.
    Returns:
        min_credits: The minimum number of credits that this section can be worth.
        max_credits: The minimum number of credits that this section can be worth.
        meetings: A list of Meeting instances.
    """
    pass    # WIP

def extract_tr_data(tr):
    """Extract section data from tr.

    Args:
        tr: A bs4.BeautifulSoup instance
    Returns:
        name: The abbreviated name of the section (used if the course doesn't exist)
        CRN: The unique Course Registration Number that identifies this section within a term.
        section_num: The section number that, when combined with a department and course number, uniquely identifies this section.
    """
    ddtitle = tr.select_one('.ddtitle')
    name, crn, section_num = parse_ddtitle(ddtitle)
    return name, crn, section_num


class Command(BaseCommand):
    help = 'Retrieves all of the sections in the Texas A&M University system'

    def handle(self, *args, **options):
        term_codes = request_term_codes()[1:]
        for term_code in term_codes[1:2]:
            depts = request_depts(term_code)
            for dept in depts[1:2]:
                soup = request_dept_sections(term_code, dept)
                outer_datadisplaytable = soup.select_one(
                    'table.datadisplaytable')
                trs = merge_trs(outer_datadisplaytable)
                for tr in trs[1:2]:
                    print(extract_tr_data(tr))
