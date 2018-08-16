from django.contrib import admin

from courses import models as course_models

# Register your models here.


@admin.register(course_models.Course)
class CourseAdmin(admin.ModelAdmin):
    pass
