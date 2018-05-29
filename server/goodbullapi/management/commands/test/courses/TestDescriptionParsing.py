import unittest
from .data import acct_file, law_file, csce_file
from _functions.functions import parse_description


class TestDescriptionParsing(unittest.TestCase):
    def set_up(self):
        self.acct_course_blocks = acct_file.select('.courseblock')
        self.csce_course_blocks = csce_file.select('.courseblock')
        self.law_course_blocks = law_file.select('.courseblock')

    def test_no_prereqs(self):
        self.set_up()
        description = self.law_course_blocks[0].select_one(
            '.courseblockdesc').get_text()
        ACTUAL = parse_description(description)
        EXPECTED = ('Rules and doctrines that define the process of civil litigation in American courts; primary emphasis on the U.S. Constitution, federal judicial code and Federal Rules of Civil Procedure; topics may include the jurisdiction and competence of courts, conflicts between state and federal law, pleading, discovery, joinder of claims and parties, disposition without trial, trial and post-trial process, appellate review, and the effects of judgment.', None, None)
        self.assertEqual(ACTUAL, EXPECTED)

    def test_prereqs_only(self):
        self.set_up()
        description = self.law_course_blocks[9].select_one(
            '.courseblockdesc').get_text()
        ACTUAL = parse_description(description)
        EXPECTED = ('Principles of testate and intestate succession; drafting, execution and construction of attested and holographic wills; testamentary capacity, undue influence and fraud; revocation of wills; distribution of intestacy; nonprobate transfers of property; ethical issues that arise during estate planning; significant focus on Texas law.',
                    'One year of law school in the full-time or part-time program; LAW 7032.', None)
        self.assertEqual(ACTUAL, EXPECTED)

    def test_prereqs_coreqs(self):
        self.set_up()
        description = self.csce_course_blocks[6].select_one(
            '.courseblockdesc').get_text()
        ACTUAL = parse_description(description)
        EXPECTED = ('Specification and implementation of basic abstract data types and their associated algorithms including stacks, queues, lists, sorting and selection, searching, graphs, and hashing; performance tradeoffs of different implementations and asymptotic analysis of running time and memory usage; includes the execution of student programs written in C++.',
                    'CSCE 113 or CSCE 121.', 'CSCE 222/ECEN 222.')
        self.assertEqual(ACTUAL, EXPECTED)
