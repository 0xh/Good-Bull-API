from django.urls import path
from rest_framework import routers

from courses import views as course_views

router = routers.DefaultRouter()
urlpatterns = [
    path('<dept>/', course_views.CourseListView.as_view()),
    path('<dept>/<course_num>/', course_views.CourseHistoricalDetailView.as_view()),
    path('<dept>/<course_num>/<int:term_code>/', course_views.CourseSemesterDetailView.as_view()),
    path('<dept>/<course_num>/<int:term_code>/<section_num>/', course_views.SectionDetailView.as_view())
]
