import requests
from bs4 import BeautifulSoup
import re

def request_html(url: str, headers: dict=None, form_data: dict=None, post: bool=False) -> BeautifulSoup:
    """Given URL to webpage, returns a BeautifulSoup containing HTML.

    Args:
        url: The URL of the webpage to request.
        headers: A dictionary containing HTTP headers to send with request.
        form_data: A dictionary of entries for form data
        post: Indicates whether or not to post
    Returns:
        A BeautifulSoup instance containing the webpage HTML.
    """
    r = None
    if not post:
        r = requests.get(url, headers=headers)
    else:
        r = requests.post(url, form_data)
    r.raise_for_status()
    html = r.text
    return BeautifulSoup(html, 'lxml')


def sanitize(string: str) -> str:
    """Takes a string and replaces Unicode characters with single spaces."""
    string = re.sub(r'\s+', ' ', string)
    return ''.join([i if ord(i) < 128 else ' ' for i in string]).strip()