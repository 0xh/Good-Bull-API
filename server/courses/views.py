from rest_framework import generics
from django.db import models as db_models
from courses import models as course_models
from courses import serializers as course_serializers
from django import shortcuts
from rest_framework import response


class CourseListView(generics.ListAPIView):
    """List all of the courses ever offered by a department. Does not include sections."""
    serializer_class = course_serializers.CourseOverviewSerializer

    def get_queryset(self):
        dept = self.kwargs['dept']
        return course_models.Course.objects.filter(dept=dept)


class CourseHistoricalDetailView(generics.RetrieveAPIView):
    """Retrieve all of the sections ever offered by a course."""
    serializer_class = course_serializers.CourseSerializer

    def get_object(self):
        fields_to_match = {
            'dept': self.kwargs['dept'],
            'course_num': self.kwargs['course_num']
        }

        return course_models.Course.objects.get(**fields_to_match)


class CourseSemesterDetailView(generics.RetrieveAPIView):
    """Retrieve all of the sections offered by a Course during a specific semester."""
    serializer_class = course_serializers.CourseSerializer

    def get_serializer_context(self):
        context = {'request': self.request}
        context['term_code'] = self.kwargs['term_code']
        return context

    def get_object(self):
        fields_to_match = {
            'dept': self.kwargs['dept'],
            'course_num': self.kwargs['course_num']
        }

        return course_models.Course.objects.get(**fields_to_match)


class SectionDetailView(generics.RetrieveAPIView):
    """Retrieve a Section offered by a Course during a specific semester."""
    serializer_class = course_serializers.SectionSerializer

    def get_object(self):
        course_fields = {
            'dept': self.kwargs['dept'],
            'course_num': self.kwargs['course_num']
        }
        course_queryset = course_models.Course.objects.all()
        course = shortcuts.get_object_or_404(course_queryset, **course_fields)

        fields_to_match = {
            'course': course,
            'term_code': self.kwargs['term_code'],
            'section_num': self.kwargs['section_num']
        }

        return course_models.Section.objects.get(**fields_to_match)
