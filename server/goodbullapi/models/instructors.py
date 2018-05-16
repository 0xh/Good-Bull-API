from django.db import models
from django.contrib.postgres.fields import ArrayField
from goodbullapi.models import Section

class GPADistribution(models.Model):
    ABCDFQ = ArrayField(models.IntegerField())
    section = models.OneToOneField(Section, on_delete=models.CASCADE)