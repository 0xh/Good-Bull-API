from goodbullapi.models import Course
from goodbullapi.serializers import CourseSerializer
from rest_framework import viewsets

class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CourseSerializer

    def get_queryset(self):
        term_code = self.kwargs['term_code']
        return Course.objects.filter(term_code=term_code)
