from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

import goodbullapi.views

urlpatterns = [
    url(r'courses/(?P<term_code>.+)/(?P<dept>.+)', goodbullapi.views.CourseList.as_view())
]