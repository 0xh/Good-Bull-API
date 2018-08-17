from django.contrib.postgres.search import SearchVectorField
from django.db import models


class Course(models.Model):
    _id = models.CharField(max_length=10, primary_key=True)
    dept = models.CharField(
        max_length=4, help_text='The abbreviation of the department offering this course.')
    course_num = models.CharField(max_length=5, help_text='The course number.')
    name = models.CharField(
        max_length=100, help_text='The name of the course.')
    distribution_of_hours = models.CharField(
        max_length=60, null=True, blank=True, help_text='How many of the hours listed will be spent in lecture, lab, etc.')
    description = models.TextField(max_length=500, null=True, blank=True,
                                   help_text='A verbose description of the course\'s purpose.')
    prereqs = models.TextField(
        null=True, blank=True, help_text='The prerequisites of the course.')
    coreqs = models.TextField(null=True, blank=True,
                              help_text='The corequisites of the course.')
    min_credits = models.FloatField(
        help_text='Minimum number of credits this course can count for.')
    max_credits = models.FloatField(
        help_text='Maximum number of credits this course can count for.')

    def __str__(self):
        return self.dept + '-' + self.course_num

    class Meta:
        ordering = ('dept', 'course_num')
        indexes = [
            models.Index(fields=['dept', 'course_num']),
            models.Index(fields=['min_credits', 'max_credits']),
            models.Index(fields=['name'])
        ]
