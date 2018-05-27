import unittest
from _functions.functions import parse_title
import requests


class TestParseTitle(unittest.TestCase):

    def test_basic_title(self):
        TEST_STRING = 'AALO 285 Directed Studies'
        EXPECTED = ('285', 'Directed Studies')
        self.assertEqual(parse_title(TEST_STRING), EXPECTED)

    def test_cross_listed(self):
        # Simple cases:
        # Four-character department abbreviations, three-character course numbers.
        TEST_STRING = 'ACCT 430/IBUS 428 Global Immersion in Accounting'
        EXPECTED = ('430', 'Global Immersion in Accounting')
        self.assertEqual(parse_title(TEST_STRING), EXPECTED)

        # Complex cases:
        # 3-number, 1-letter course numbers
        TEST_STRING = 'EXAM 123S/EXAM 789 Cross-listed example 1'
        EXPECTED = ('123S', 'Cross-listed example 1')
        self.assertEqual(parse_title(TEST_STRING), EXPECTED)

        TEST_STRING = 'EXAM 123/EXAM 789S Cross-listed example 2'
        EXPECTED = ('123', 'Cross-listed example 2')
        self.assertEqual(parse_title(TEST_STRING), EXPECTED)

        # 4-number course numbers
        TEST_STRING = 'EXAM 1234/EXAM 789 Cross-listed example 3'
        EXPECTED = ('1234', 'Cross-listed example 3')
        self.assertEqual(parse_title(TEST_STRING), EXPECTED)

        TEST_STRING = 'EXAM 123/EXAM 7890 Cross-listed example 4'
        EXPECTED = ('123', 'Cross-listed example 4')
        self.assertEqual(parse_title(TEST_STRING), EXPECTED)

        # 3-letter dept
        TEST_STRING = 'LAW 123/EXAM 123S Cross-listed example 5'
        EXPECTED = ('123', 'Cross-listed example 5')
        self.assertEqual(parse_title(TEST_STRING), EXPECTED)

if __name__ == '__main__':
    unittest.main()
