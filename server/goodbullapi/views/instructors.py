from rest_framework import generics
from goodbullapi.models import Instructor
from goodbullapi.serializers import InstructorSerializer
from django.shortcuts import get_object_or_404


class InstructorRetrieve(generics.RetrieveAPIView):
    """
    Retrieves an instructor (and their associated sections) based on their ID.
    IDs are simply LASTNAME_FIRSTINITIAL.
    """
    serializer_class = InstructorSerializer
    queryset = Instructor.objects.all()


class InstructorListByCourse(generics.ListAPIView):
    """
    Given a department and course number, retrieves all of the instructors who have
    ever taught that course. Useful for comparing instructors to one another in terms
    of how they grade a course.
    """
    serializer_class = InstructorSerializer

    def get_queryset(self):
        dept = self.kwargs['dept']
        course_num = self.kwargs['course_num']
        queryset = Instructor.objects.filter(
            sections_taught__section__dept=dept, sections_taught__section__course_num=course_num)
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset
