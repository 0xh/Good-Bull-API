from django.urls import path
from instructors import views as instructor_views
urlpatterns = [
    path('<int:pk>/', instructor_views.InstructorRetrieveView.as_view())
]
