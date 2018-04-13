from django.db import models
from django.contrib.postgres.fields import ArrayField
# Create your models here.


class Course(models.Model):
    _id = models.CharField(primary_key=True, max_length=16)
    short = models.CharField(max_length=12)
    term_code = models.CharField(max_length=6)
    name = models.CharField(max_length=125)
    credits = models.IntegerField()
    description = models.TextField(max_length=300)
    division_of_hours = models.TextField(max_length=100)
    prereqs = models.TextField(max_length=150, null=True)

    class Meta:
        ordering = ('_id',)
