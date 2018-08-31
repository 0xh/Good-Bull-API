from django.contrib import admin

from courses import models as course_models

# Register your models here.


admin.site.register(course_models.Course)
admin.site.register(course_models.GradeDistribution)
admin.site.register(course_models.Meeting)
admin.site.register(course_models.Section)
