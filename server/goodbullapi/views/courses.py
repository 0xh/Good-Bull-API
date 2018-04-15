from goodbullapi.models import Course
from goodbullapi.serializers import CourseSerializer
from rest_framework import generics

class CourseList(generics.ListAPIView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        term_code = self.kwargs['term_code']
        dept = self.kwargs['dept']
        queryset = Course.objects.filter(term_code=term_code, dept=dept)
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset