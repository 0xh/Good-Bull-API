from django.db import models
from django.contrib.postgres.search import SearchVectorField


class Instructor(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    searchable_field = models.CharField(max_length=200)
    search_vector = SearchVectorField()

    class Meta:
        ordering = ('lastname', 'firstname')
