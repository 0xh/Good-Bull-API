import codecs
import csv
import urllib

import requests


def request_html(url):
    """
    Given a URL, makes a request to that
    URL, and returns the HTML.
    """


def stream_csv(url):
    """
    Generator function.
    Given a URL, makes a request to that URL,
    and yield each non-header row of the CSV.
    """
    file_stream = urllib.request.urlopen(url)
    csvfile = csv.reader(codecs.iterdecode(file_stream, 'utf-8'))
    next(csvfile)
    for row in csvfile:
        yield row
