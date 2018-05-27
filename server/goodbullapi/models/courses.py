from django.db import models


class Course(models.Model):
    _id = models.CharField(max_length=10, primary_key=True)
    dept = models.CharField(max_length=4)
    course_num = models.CharField(max_length=5)
    name = models.CharField(max_length=100)
    distribution_of_hours = models.CharField(max_length=60)
    description = models.TextField(max_length=500)
    prereqs = models.TextField(null=True)
    coreqs = models.TextField(null=True)
    min_credits = models.IntegerField(verbose_name='Minimum number of credits this course can count for')
    max_credits = models.IntegerField(verbose_name='Maximum number of credits this course can count for')


    class Meta:
        ordering = ('dept', 'course_num')
