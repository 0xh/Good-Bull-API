import datetime
import os
import unittest

import bs4

from sections.management.commands.parser import body_functions
from sections.tests.management_commands_tests.parser_tests import parser_testcase


class BodyFunctionsTestCase(parser_testcase.ParserTestCase):

    def setUp(self):
        self.instructor1_name = 'John Doe (P)'
        self.instructor2_name = 'Jane Doe-Biff'
        self.instructor_names = [self.instructor1_name, self.instructor2_name]

    def test_has_primary_indicator(self):
        actual = body_functions.has_primary_indicator(self.instructor1_name)
        self.assertTrue(actual)

        actual = body_functions.has_primary_indicator(self.instructor2_name)
        self.assertFalse(actual)

    def test_strip_primary_indicator(self):
        expected = 'John Doe'
        actual = body_functions.strip_primary_indicator(self.instructor1_name)
        self.assertEqual(expected, actual)

        expected = 'Jane Doe-Biff'
        actual = body_functions.strip_primary_indicator(self.instructor2_name)
        self.assertEqual(expected, actual)

    def test_parse_hours(self):
        soup = self.open_mock_html_file('dddefault_normal.html')
        expected_min, expected_max = 3.0, 3.0
        actual_min, actual_max = body_functions.parse_hours(soup)
        self.assertEqual(expected_min, actual_min)
        self.assertEqual(expected_max, actual_max)

    def test_parse_hours_variable_hours(self):
        soup = self.open_mock_html_file('dddefault_variable_hours.html')
        expected_min, expected_max = 0.0, 4.0

        actual_min, actual_max = body_functions.parse_hours(soup)
        self.assertEqual(expected_min, actual_min)
        self.assertEqual(expected_max, actual_max)

    def test_parse_hours_no_hours(self):
        soup = self.open_mock_html_file('dddefault_no_hours.html')
        expected_min, expected_max = None, None
        actual_min, actual_max = body_functions.parse_hours(soup)

        self.assertEqual(expected_min, actual_min)
        self.assertEqual(actual_min, actual_max)

    def test_parse_duration(self):
        dummy_string = '7:15 pm - 9:15 pm'
        expected_start = datetime.datetime(1900, 1, 1, hour=19, minute=15)
        expected_end = datetime.datetime(1900, 1, 1, hour=21, minute=15)

        actual_start, actual_end = body_functions.parse_duration(dummy_string)

        self.assertTupleEqual(
            (expected_start, expected_end), (actual_start, actual_end))

    def test_parse_duration_when_tba(self):
        dummy_string = 'TBA'

        expected_start_end = (None, None)

        actual_start_end = body_functions.parse_duration(dummy_string)

        self.assertTupleEqual(expected_start_end, actual_start_end)

    def test_parse_datadisplaytable(self):
        soup = self.open_mock_html_file('dddefault_normal.html')
        expected_meetings = [
            {
                'location': 'Wehner - College of Business 113',
                'meeting_type': 'Lecture',
                'meeting_days': 'R',
                'start_time': datetime.datetime(1900, 1, 1, hour=8),
                'end_time': datetime.datetime(1900, 1, 1, hour=9, minute=15)
            },
            {
                'location': None,
                'meeting_type': 'Examination',
                'meeting_days': 'R',
                'start_time': datetime.datetime(1900, 1, 1, hour=19, minute=15),
                'end_time': datetime.datetime(1900, 1, 1, hour=21, minute=15)
            },
            {
                'location': None,
                'meeting_type': 'Examination',
                'meeting_days': 'R',
                'start_time': datetime.datetime(1900, 1, 1, hour=19, minute=15),
                'end_time': datetime.datetime(1900, 1, 1, hour=21, minute=15)
            },
            {
                'location': None,
                'meeting_type': 'Examination',
                'meeting_days': 'R',
                'start_time': datetime.datetime(1900, 1, 1, hour=19, minute=15),
                'end_time': datetime.datetime(1900, 1, 1, hour=21, minute=15)
            }
        ]

        expected_mentioned_instructors = ['Mary Knetsar Stasny (P)',
                                          'Mary Knetsar Stasny (P)',
                                          'Mary Knetsar Stasny (P)',
                                          'Mary Knetsar Stasny (P)']

        actual_meetings, actual_mentioned_instructors = body_functions.parse_datadisplaytable(
            soup)

        self.assertEqual(expected_meetings, actual_meetings)
        self.assertListEqual(expected_mentioned_instructors,
                             actual_mentioned_instructors)
