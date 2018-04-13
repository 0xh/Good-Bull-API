from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from sections import views

router = DefaultRouter()
router.register(r'', views.SectionViewSet)

urlpatterns = [
        url(r'^', include(router.urls))
]
