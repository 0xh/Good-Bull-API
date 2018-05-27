from datetime import datetime

from django.contrib.postgres.search import SearchVectorField
from django.db import models


class Building(models.Model):
    abbr = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=50)
    location_description = models.CharField(max_length=40)

    FOUNDING_YEAR = 1871
    THIS_YEAR = datetime.now().year + 1
    YEAR_CHOICES = [(r, r) for r in range(FOUNDING_YEAR, THIS_YEAR)]
    year_built = models.IntegerField(choices=YEAR_CHOICES, null=True)

    FLOOR_CHOICES = [(r, r) for r in range(1, 20)]
    num_floors = models.IntegerField(choices=FLOOR_CHOICES, null=True)

    address = models.CharField(max_length=100)
    city = models.CharField(max_length=40)
    zip_code = models.CharField(max_length=11)
    searchable_field = models.CharField(max_length=61)
    search_vector = SearchVectorField()

    class Meta:
        ordering = ('abbr',)
