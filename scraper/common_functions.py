import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
}


def get_term_codes():
    URL = 'https://compass-ssb.tamu.edu/pls/PROD/bwckschd.p_disp_dyn_sched'
    r = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(r.text, 'html.parser')
    options = soup.find_all('option', {'value': True})
    options = options[1:]
    return [option['value'] for option in options]


def get_depts(term_code):
    URL = 'https://compass-ssb.tamu.edu/pls/PROD/bwckgens.p_proc_term_date'
    FORM_DATA = {
        'p_calling_proc': 'bwckschd.p_disp_dyn_sched',
        'p_term': term_code
    }
    response = requests.post(URL, FORM_DATA)
    soup = BeautifulSoup(response.text, 'html.parser')
    return [option['value']
            for option in soup.find(id='subj_id').find_all('option')]
