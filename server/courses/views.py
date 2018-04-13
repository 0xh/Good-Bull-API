from django.shortcuts import render
from rest_framework import viewsets
from courses.models import Course
from courses.serializers import CourseSerializer

# Create your views here.


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
