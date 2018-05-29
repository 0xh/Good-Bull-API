import unittest
from .data import acct_file, law_file
from _functions.functions import sanitize


class TestSanitization(unittest.TestCase):
    def set_up(self):
        self.course_blocks = acct_file.select('.courseblock')

    def test_sanitization(self):
        self.set_up()
        name = self.course_blocks[0].select_one(
            '.courseblocktitle').get_text().strip()
        ACTUAL = sanitize(name)
        EXPECTED = 'ACCT 209 Survey of Accounting Principles'
        self.assertEqual(ACTUAL, EXPECTED)
