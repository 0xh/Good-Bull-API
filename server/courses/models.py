from django.contrib.postgres.search import SearchVectorField
from django.db import models


class Course(models.Model):
    _id = models.CharField(max_length=10, primary_key=True)
    dept = models.CharField(max_length=4)
    course_num = models.CharField(max_length=5)
    name = models.CharField(max_length=100)
    distribution_of_hours = models.CharField(
        max_length=60, null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    prereqs = models.TextField(null=True, blank=True)
    coreqs = models.TextField(null=True, blank=True)
    min_credits = models.FloatField(
        verbose_name='Minimum number of credits this course can count for')
    max_credits = models.FloatField(
        verbose_name='Maximum number of credits this course can count for')

    def __str__(self):
        return self.dept + '-' + self.course_num

    class Meta:
        ordering = ('dept', 'course_num')