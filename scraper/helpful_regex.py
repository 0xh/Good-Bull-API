import re
TITLE_PATTERN = re.compile(
    '(?P<section_name>.+) - (?P<crn>.+) - (?P<dept>.+) (?P<course_num>.+) - (?P<section_num>[^ \(]+)')

REGULAR_CREDITS_PATTERN = re.compile('(?P<lower_bound_credits>.+) ')
VARYING_CREDITS_PATTERN = re.compile(
    '(?P<least_credits>.+) (?:TO|OR) (?P<most_credits>.+) ')

INSTRUCTOR_PATTERN = re.compile(
    '(?:Instructor:|Instructors:) (?P<instructors>[\w .-]+)(?:,| \(P\)| College| Galveston| Qatar)')

COURSE_EXTRACT_TITLE = re.compile('(?<=\d{3} ).*')
