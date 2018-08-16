from django.contrib import admin
from instructors import models as instructor_models
# Register your models here.


@admin.register(instructor_models.Instructor)
class InstructorAdmin(admin.ModelAdmin):
    pass
