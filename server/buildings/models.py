import datetime

from django.db import models

# Create your models here.


class Building(models.Model):
    """A representation of a TAMU-owned building.

    Attributes:
        abbr: The building abbreviation (primary key)
        name: The name of the building
        location_description: A description of the location
        year_built: What year it was built
        num_floors: How many floors there are
        address: The street address
        city: The city it's in
        zip_code: The zip code it's in
    """
    abbr = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=50)
    location_description = models.CharField(max_length=40)

    FOUNDING_YEAR = 1871
    year_built = models.IntegerField(null=True, blank=True)

    num_floors = models.IntegerField(null=True, blank=True)

    address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=40, blank=True)
    zip_code = models.CharField(max_length=11, blank=True)

    def __str__(self):
        return self.abbr

    class Meta:
        ordering = ('abbr',)
