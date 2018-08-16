from django.contrib import admin

from buildings import models as building_models

# Register your models here.


@admin.register(building_models.Building)
class BuildingAdmin(admin.ModelAdmin):
    pass
