from sections.management.commands.parser import title_functions
from sections.tests.management_commands_tests.parser_tests import \
    parser_testcase


class TitleFunctionsTestCase(parser_testcase.ParserTestCase):
    def test_is_honors(self):
        dummy_section_num = '201'
        dummy_name = 'FOO BAR'
        self.assertTrue(title_functions.is_honors(
            dummy_name, dummy_section_num))

    def test_is_honors_num_false(self):
        dummy_section_num = '501'
        dummy_name = 'HNR- FOO BAR'
        self.assertTrue(title_functions.is_honors(
            dummy_name, dummy_section_num))

    def test_is_honors_is_false(self):
        dummy_section_num = '501'
        dummy_name = 'FOO BAR'
        self.assertFalse(title_functions.is_honors(
            dummy_name, dummy_section_num))

    def test_is_sptp(self):
        dummy_course_nums = ['289', '489', '689']
        dummy_name = 'NAME WITHOUT SPTP:'
        for course_number in dummy_course_nums:
            self.assertTrue(title_functions.is_sptp(dummy_name, course_number))

    def test_is_not_sptp(self):
        dummy_course_num = '688'
        dummy_name = 'SPT: INTENTIONAL TYPO'
        self.assertFalse(title_functions.is_sptp(dummy_name, dummy_course_num))

    def test_strip_honors_prefix(self):
        honors_name = 'HNR-NAME GOES HERE'
        expected = 'NAME GOES HERE'
        actual = title_functions.strip_honors_prefix(honors_name)
        self.assertEqual(expected, actual)

        non_honors_name = 'DUMMY NAME'
        expected = 'DUMMY NAME'
        actual = title_functions.strip_honors_prefix(non_honors_name)
        self.assertEqual(expected, actual)

    def test_strip_honors_prefix_when_doesnt_start_with_hnr(self):
        non_honors_name = 'SOMEHOW HNR-HERE'
        expected = 'SOMEHOW HNR-HERE'
        actual = title_functions.strip_honors_prefix(non_honors_name)
        self.assertEqual(expected, actual)

    def test_strip_sptp_prefix(self):
        sptp_name = 'SPTP:SPECIAL TOPICS COURSE'
        expected = 'SPECIAL TOPICS COURSE'
        actual = title_functions.strip_sptp_prefix(sptp_name)
        self.assertEqual(expected, actual)

        non_sptp_name = 'NOT SPECIAL TOPICS COURSE'
        expected = 'NOT SPECIAL TOPICS COURSE'
        actual = title_functions.strip_sptp_prefix(non_sptp_name)
        self.assertEqual(expected, actual)

    def test_strip_sptp_prefix_if_not_sptp(self):
        non_sptp_name = 'NOT SPECIAL TOPICS BUT SPTP: PRESENT'
        expected = 'NOT SPECIAL TOPICS BUT SPTP: PRESENT'
        actual = title_functions.strip_honors_prefix(non_sptp_name)

        self.assertEqual(expected, actual)

    def test_parse_dddefault(self):
        soup = self.open_mock_html_file('dddtitle_normal.html')
        expected = ('DUAL LANGUAGE PROG METHD', 15254, '611', '699')
        actual = title_functions.parse_ddtitle(soup)

        self.assertTupleEqual(expected, actual)
