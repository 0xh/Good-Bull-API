from rest_framework import routers
from goodbullapi import views
from django.conf.urls import url, include

router = routers.DefaultRouter()
router.register(r'buildings', views.BuildingViewSet)

urlpatterns = [
    url(r'^courses/(?P<dept>.+)/(?P<course_num>.+)/', views.CourseRetrieve.as_view()),
    url(r'^courses/(?P<dept>.+)/', views.DepartmentList.as_view()),
    url(r'^', include(router.urls))
]
