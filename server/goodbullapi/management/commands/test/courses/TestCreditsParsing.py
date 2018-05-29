import unittest

from _functions.functions import parse_credits

from .data import acct_file, csce_file, law_file


class TestCreditsParsing(unittest.TestCase):
    def set_up(self):
        self.acct_course_blocks = acct_file.select('.courseblock')
        self.csce_course_blocks = csce_file.select('.courseblock')
        self.law_course_blocks = law_file.select('.courseblock')

    def test_basic_credits(self):
        self.set_up()
        credits = self.csce_course_blocks[0].select_one('.hours').get_text()
        ACTUAL = parse_credits(credits)
        EXPECTED = (4, 4)
        self.assertEqual(ACTUAL, EXPECTED)

    def test_varying_to_credits(self):
        self.set_up()
        credits = self.csce_course_blocks[-2].select_one('.hours').get_text()
        ACTUAL = parse_credits(credits)
        EXPECTED = (1, 4)
        self.assertEqual(ACTUAL, EXPECTED)

    def test_varying_or_credits(self):
        self.set_up()
        credits = 'Credits 2 or 3.'
        ACTUAL = parse_credits(credits)
        EXPECTED = (2, 3)
        self.assertEqual(ACTUAL, EXPECTED)
