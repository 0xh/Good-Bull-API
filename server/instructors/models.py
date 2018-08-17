from django.db import models


class Instructor(models.Model):
    name = models.CharField(
        max_length=200, help_text='The name of the instructor.')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
