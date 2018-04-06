from django.db import models

# Create your models here.
class Course(models.Model):
    _id = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=40)
    description = models.TextField(max_length=300)
    division_of_hours = models.TextField(max_length=100)
    prereqs = models.TextField(max_length=150)
    class Meta:
        ordering=('_id',)
