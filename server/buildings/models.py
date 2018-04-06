from django.db import models

# Create your models here.
class Building(models.Model):
    abbr = models.CharField(primary_key=True, max_length=5)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=11)

    class Meta:
        ordering = ('abbr',)
