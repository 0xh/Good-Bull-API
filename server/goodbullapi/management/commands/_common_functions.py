import requests
from bs4 import BeautifulSoup


def request_html(url: str, headers: dict=None) -> BeautifulSoup:
    """Given URL to webpage, returns a BeautifulSoup containing HTML.

    Args:
        url: The URL of the webpage to request.
        headers: A dictionary containing HTTP headers to send with request.
    Returns:
        A BeautifulSoup instance containing the webpage HTML.
    """
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    html = r.text
    return BeautifulSoup(html, 'lxml')
