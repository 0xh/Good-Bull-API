import os
import unittest

import bs4


class ParserTestCase(unittest.TestCase):
    MOCKS_DIRECTORY = os.path.abspath(
        'server/sections/tests/management_commands_tests/parser_tests/mocks/')

    def open_mock_html_file(self, filename):
        file = open(os.path.join(self.MOCKS_DIRECTORY, filename))
        return bs4.BeautifulSoup(file, 'html.parser')
