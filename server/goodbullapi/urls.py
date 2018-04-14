from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

import goodbullapi.views

router = DefaultRouter()
router.register(r'courses/(?P<term_code>.+)', goodbullapi.views.CourseViewSet, base_name='Course')
router.register(r'buildings', goodbullapi.views.BuildingViewSet)
router.register(r'sections', goodbullapi.views.SectionViewSet)
urlpatterns = [
    url('^', include(router.urls))
]