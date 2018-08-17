import datetime
import unittest

from instructors.management.commands import parser


class ParserTestCase(unittest.TestCase):

    def test_generate_term_codes(self):
        term_codes = []
        for i in range(datetime.datetime.now().year, 2012, -1):
            for j in range(1, 4):
                term_codes.append(str(i) + str(j))
        self.assertListEqual(term_codes, list(parser.generate_term_codes()))
