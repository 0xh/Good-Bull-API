from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from buildings import views

router = DefaultRouter()
router.register(r'', views.BuildingViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]
