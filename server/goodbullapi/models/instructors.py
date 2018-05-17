from django.db import models
from django.contrib.postgres.fields import ArrayField
from goodbullapi.models import Section


class GPADistribution(models.Model):
    ABCDFQ = ArrayField(models.IntegerField())
    gpa = models.FloatField(verbose_name="The overall course GPA.")
    section = models.OneToOneField(
        Section, on_delete=models.CASCADE, related_name="gpa_distribution")
    instructor = models.ForeignKey(
       'Instructor', on_delete=models.CASCADE, related_name='sections_taught', null=True)

    def __repr__(self):
        return str(self.ABCDFQ) + " " + str(self.section) + " " + str(self.instructor)


class Instructor(models.Model):
    name = models.CharField(max_length=70)
    
    def __repr__(self):
        return self.name.to_python()
