from goodbullapi.models import Course
from goodbullapi.serializers import CourseSerializer
from rest_framework import generics
from django.shortcuts import get_object_or_404

class CourseListByDepartment(generics.ListAPIView):
    """
    Lists all courses offered by a department during a term, to allow for larger searches 
    while not slowing down retrieval (this search is still slow for larger departments).
    """

    serializer_class = CourseSerializer

    def get_queryset(self):
        term_code = self.kwargs['term_code']
        dept = self.kwargs['dept']
        queryset = Course.objects.filter(term_code=term_code, dept=dept)
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset

class CourseRetrieve(generics.RetrieveAPIView):
    """
    Retrieves a specific course offered during a term.
    """
    
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.get_serializer_class().setup_eager_loading(queryset)

        filter = {
            'term_code': self.kwargs['term_code'],
            'dept': self.kwargs['dept'],
            'course_num': self.kwargs['course_num']
        }
        return get_object_or_404(queryset, **filter)

