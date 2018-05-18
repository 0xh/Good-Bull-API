from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

import goodbullapi.views

router = DefaultRouter()
router.register(r'', goodbullapi.views.BuildingViewSet)

urlpatterns = [
    url(r'buildings/', include(router.urls)),

    url(r'courses/(?P<term_code>.+)/(?P<dept>.+)/(?P<course_num>.+)/$', goodbullapi.views.CourseRetrieve.as_view()),
    url(r'courses/(?P<term_code>.+)/(?P<dept>.+)/$', goodbullapi.views.CourseList.as_view()),

    url(r'sections/(?P<term_code>.+)/(?P<crn>.+)/$', goodbullapi.views.SectionRetrieve.as_view()),
    url(r'instructors/(?P<dept>.+)/(?P<course_num>.+)/$', goodbullapi.views.InstructorListByCourse.as_view()),
    url(r'instructors/(?P<pk>.+)/$', goodbullapi.views.InstructorRetrieve.as_view())
]