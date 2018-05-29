import os
from bs4 import BeautifulSoup
acct_file = law_file = csce_file = None

THIS_DIR = os.path.dirname(__file__)

ACCT_FILE_PATH = os.path.join(THIS_DIR, 'acct-catalog.html')
LAW_FILE_PATH = os.path.join(THIS_DIR, 'law-catalog.html')
CSCE_FILE_PATH = os.path.join(THIS_DIR, 'csce-catalog.html')

with open(ACCT_FILE_PATH, 'r') as f:
    acct_file = BeautifulSoup(f.read(), 'lxml')
with open(LAW_FILE_PATH, 'r') as f:
    law_file = BeautifulSoup(f.read(), 'lxml')
with open(CSCE_FILE_PATH, 'r') as f:
    csce_file = BeautifulSoup(f.read(), 'lxml')
__all__ = ['acct_file', 'law_file', 'csce_file']
