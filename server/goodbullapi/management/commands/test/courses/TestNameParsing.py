import unittest
from .data import acct_file, law_file, csce_file
from _functions.functions import parse_name


class TestNameParsing(unittest.TestCase):
    """
    Tests the `parse_name` function on various names present in the catalog.
    """

    def set_up(self):
        self.acct_course_blocks = acct_file.select('.courseblock')
        self.law_course_blocks = law_file.select('.courseblock')
        self.csce_course_blocks = csce_file.select('.courseblock')

    def test_simple_name(self):
        self.set_up()
        name = self.acct_course_blocks[0].select_one(
            '.courseblocktitle').get_text()
        ACTUAL = parse_name(name)
        EXPECTED = ('209', 'Survey of Accounting Principles')
        self.assertEqual(ACTUAL, EXPECTED)

    def test_four_digit(self):
        self.set_up()
        name = self.law_course_blocks[128].select_one(
            '.courseblocktitle').get_text()
        ACTUAL = parse_name(name)
        EXPECTED = ('7122', 'Agency and Partnership')
        self.assertEqual(ACTUAL, EXPECTED)

    def test_five_digit(self):
        self.set_up()
        name = self.law_course_blocks[324].select_one(
            '.courseblocktitle').get_text()
        ACTUAL = parse_name(name)
        EXPECTED = ('7863S', 'Criminal Prosecution Clinic')
        self.assertEqual(ACTUAL, EXPECTED)

    def test_cross_listed(self):
        self.set_up()
        name = self.csce_course_blocks[41].select_one(
            '.courseblocktitle').get_text()
        ACTUAL = parse_name(name)
        EXPECTED = ('461', 'Embedded Systems for Medical Applications')
        self.assertEqual(ACTUAL, EXPECTED)
