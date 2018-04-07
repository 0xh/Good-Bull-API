from django.db import models

# Create your models here.
class Course(models.Model):
    _id = models.CharField(primary_key=True, max_length=10)
    short = models.CharField(max_length=8)
    term_code = models.CharField(max_length=6)
    name = models.CharField(max_length=40)
    credits = models.IntegerField()
    description = models.TextField(max_length=300)
    division_of_hours = models.TextField(max_length=100)
    prereqs = models.TextField(max_length=150, null=True)
    class Meta:
        ordering=('_id',)
