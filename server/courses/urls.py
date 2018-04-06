from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from courses import views

router = DefaultRouter()
router.register(r'courses', views.CourseViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]
