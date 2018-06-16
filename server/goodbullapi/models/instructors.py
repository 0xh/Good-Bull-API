from django.db import models
from django.contrib.postgres.search import SearchVectorField


class Instructor(models.Model):
    name = models.CharField(max_length=200)
    searchable_field = models.CharField(max_length=200)
    search_vector = SearchVectorField()

    class Meta:
        ordering = ('name',)
