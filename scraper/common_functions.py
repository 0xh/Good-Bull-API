import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
}


def request_term_codes():
    """
    Requests all of the term codes available on compass.
    Ignores professional years and half-year terms.
    """
    URL = 'https://compass-ssb.tamu.edu/pls/PROD/bwckschd.p_disp_dyn_sched'
    r = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(r.text, 'html.parser')
    options = soup.find_all('option', {'value': True})

    # Offset from the end of the list of term codes
    FIRST_TERM_2013 = -36

    # Offset from the beginning of the list of term codes
    CURRENT_TERM = 12

    options = [option['value']
               for option in options[CURRENT_TERM:FIRST_TERM_2013]]
    for term_code in options:
        # Term codes are broken up into 6-digit numbers as follows
        # XXXXYZ
        # - XXXX is the year the term occurred in
        # - Y is the semester (Spring = 1, Summer = 2, Fall = 3)
        # - Z is the campus that this term took place in
        CAMPUS = -2
        SEMESTER = -1
        # XXXXX5 means full-year professional (not relevant)
        # XXXX4X means half-year term (also not relevant)
        FULL_YEAR_PROFESSIONAL = '4'
        HALF_YEAR_TERM = '5'
        if term_code[CAMPUS] != FULL_YEAR_PROFESSIONAL and term_code[SEMESTER] != HALF_YEAR_TERM:
            yield term_code


def request_depts(term_code):
    """
    Given a term code, retrieves all of the department
    abbreviations that existed for that term.
    """
    URL = 'https://compass-ssb.tamu.edu/pls/PROD/bwckgens.p_proc_term_date'
    FORM_DATA = {
        'p_calling_proc': 'bwckschd.p_disp_dyn_sched',
        'p_term': term_code
    }
    response = requests.post(URL, FORM_DATA)
    soup = BeautifulSoup(response.text, 'html.parser')
    return [option['value']
            for option in soup.find(id='subj_id').find_all('option')]
