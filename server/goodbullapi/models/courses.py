from django.db import models

# Create your models here.
class Course(models.Model):
    _id = models.CharField(primary_key=True, max_length=16)
    dept = models.CharField(max_length=5, db_index=True)
    course_num = models.CharField(max_length=5)
    short = models.CharField(max_length=12)
    term_code = models.CharField(max_length=6, db_index=True)
    name = models.CharField(max_length=125, default='', db_index=True)
    credits = models.IntegerField(null=True)
    description = models.TextField(max_length=300, null=True)
    division_of_hours = models.TextField(max_length=100, null=True)
    prereqs = models.TextField(max_length=150, null=True)

    class Meta:
        unique_together = ('dept', 'course_num', 'term_code')
        ordering = ('_id',)