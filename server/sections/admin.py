from django.contrib import admin

from sections import models as section_models

# Register your models here.


@admin.register(section_models.Section)
class SectionAdmin(admin.ModelAdmin):
    pass


@admin.register(section_models.Meeting)
class MeetingAdmin(admin.ModelAdmin):
    pass
