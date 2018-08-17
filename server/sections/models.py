from collections import Counter
from functools import reduce

from django.core.exceptions import ValidationError
from django.contrib.postgres import fields as postgres_fields
from django.db import models


def is_valid_meeting_string(string):
    ERROR_MESSAGE = '{string} is not a valid meeting string.'.format(
        string=string)
    if not string:
        raise ValidationError('Meeting string cannot be empty.')
    """
    Enures that only the characters
    M, T, W, R, F, S, U appear in the string,
    and each character only appears once.
    """
    MONDAY = 'M'
    TUESDAY = 'T'
    WEDNESDAY = 'W'
    THURSDAY = 'R'
    FRIDAY = 'F'
    SATURDAY = 'S'
    SUNDAY = 'U'
    DAYS_OF_WEEK = [MONDAY, TUESDAY, WEDNESDAY,
                    THURSDAY, FRIDAY, SATURDAY, SUNDAY]
    day_counts = Counter(string)
    is_valid = reduce(lambda x, y: x and y, [
                      day_counts[day] <= 1 and day in DAYS_OF_WEEK for day in string])
    if not is_valid:
        raise ValidationError(ERROR_MESSAGE)


class Meeting(models.Model):
    location = models.CharField(max_length=100, null=True, blank=True)
    meeting_days = models.CharField(max_length=7, validators=[
        is_valid_meeting_string])
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)

    LECTURE = 'Lec'
    LABORATORY = 'Lab'
    RECITATION = 'Rec'
    EXAMINATION = 'Exa'
    DISSERTATION = 'Dis'
    INDEPENDENT_STUDY = 'Ind'
    RESEARCH = 'Res'

    MEETING_TYPE_CHOICES = [(LECTURE, 'Lecture'),
                            (LABORATORY, 'Laboratory'),
                            (RECITATION, 'Recitation'),
                            (EXAMINATION, 'Examination'),
                            (DISSERTATION, 'Dissertation'),
                            (INDEPENDENT_STUDY, 'Independent Study'),
                            (RESEARCH, 'Research')]
    meeting_type = models.CharField(
        choices=MEETING_TYPE_CHOICES, null=True, max_length=20)


class GradeDistribution(models.Model):
    ABCDFQISUQX = postgres_fields.ArrayField(models.IntegerField())
    gpa = models.FloatField(verbose_name='Overall section GPA')

    def __str__(self):
        return str(self.ABCDFQISUQX) + ' ' + str(self.gpa)


class Section(models.Model):
    """A representation of a Texas A&M University course section.

    Attributes:
        name: The name of the section (useful for special topics sections)
        crn: The unique Course Registration Number of the section
        course: A ForeignKey connection to the parent course of this section.
        section_num: The section number of this section
        term_code: The term in which this section was offered
        instructor: A ForeignKey connection to the instructor that taught this class.
        meetings: A ManyToMany connection to Meetings instances.
        grade_distribution: A OneToOne connection to a GradeDistribution instance.
    """

    _id = models.CharField(
        max_length=13, primary_key=True)
    name = models.CharField(
        max_length=75, help_text='The name of the section. Helpful for special topics courses.')
    crn = models.IntegerField(
        help_text='Course registration number that, when combined with termCode, uniquely identifies a section.')
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE,
                               related_name='sections', help_text='The course that this section falls under.')
    section_num = models.CharField(
        max_length=5, help_text='The section number.')
    term_code = models.IntegerField(
        help_text='The term in which this course was offered.')
    instructor = models.ForeignKey('instructors.Instructor', on_delete=models.CASCADE, related_name='sections_taught',
                                   null=True, blank=True, help_text='The instructor that taught this section.')
    meetings = models.ManyToManyField(
        Meeting, related_name='meetings', help_text='Information about when this section meets.')
    grade_distribution = models.OneToOneField(GradeDistribution, related_name='section', null=True, blank=True,
                                              on_delete=models.deletion.CASCADE, help_text='Information about the grades achieved by students in this section.')

    def __str__(self):
        return str(self.course) + '-' + self.section_num + ' Term: ' + str(self.term_code)

    class Meta:
        ordering = ('course', 'section_num')
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['course', 'section_num']),
            models.Index(fields=['term_code']),
            models.Index(fields=['grade_distribution']),
        ]
