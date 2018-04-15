from goodbullapi.models import Course
from goodbullapi.serializers import CourseSerializer
from rest_framework import viewsets

class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
