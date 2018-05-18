from rest_framework import generics
from goodbullapi.models import Instructor
from goodbullapi.serializers import InstructorSerializer
from django.shortcuts import get_object_or_404


class InstructorRetrieve(generics.RetrieveAPIView):
    serializer_class = InstructorSerializer
    queryset = Instructor.objects.all()


class InstructorListByCourse(generics.ListAPIView):
    serializer_class = InstructorSerializer

    def get_queryset(self):
        dept = self.kwargs['dept']
        course_num = self.kwargs['course_num']
        queryset = Instructor.objects.filter(
            sections_taught__section__dept=dept, sections_taught__section__course_num=course_num)
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset
