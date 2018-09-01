from django.urls import path
from rest_framework import routers

from courses import views as course_views

router = routers.DefaultRouter()
urlpatterns = [
    path('<dept>/', course_views.CourseListView.as_view(), name='course-list'),
    path('<dept>/<course_num>/', course_views.CourseDetailView.as_view(), name='course-detail'),
    path('<dept>/<course_num>/<section_num>/', course_views.SectionView.as_view(), name='section-filter')
]
