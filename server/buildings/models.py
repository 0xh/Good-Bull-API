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
    abbr = models.CharField(primary_key=True, max_length=10,
                            help_text='The building\'s abbreviation.')
    name = models.CharField(
        max_length=50, help_text='The name of the building.')
    location_description = models.CharField(
        max_length=40, help_text='A general description of where the building is located.')

    FOUNDING_YEAR = 1871
    year_built = models.IntegerField(
        null=True, blank=True, help_text='The year the building was built.')

    num_floors = models.IntegerField(
        null=True, blank=True, help_text='The number of floors of the building.')

    address = models.CharField(
        max_length=100, blank=True, help_text='The street address of the building.')
    city = models.CharField(max_length=40, blank=True,
                            help_text='The city in which the building is located.')
    zip_code = models.CharField(
        max_length=11, blank=True, help_text='The zip code in which the building is located.')

    def __str__(self):
        return self.abbr

    class Meta:
        ordering = ('abbr',)
