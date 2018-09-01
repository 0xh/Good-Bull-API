from django import shortcuts
from django.db import models as db_models
from django.http import response as http_response
from rest_framework import generics, response, views

from courses import models as course_models
from courses import serializers as course_serializers
import datetime


class CourseListView(generics.ListAPIView):
    """List all of the courses ever offered by a department. Does not include sections."""
    serializer_class = course_serializers.CourseOverviewSerializer

    def get_queryset(self):
        dept = self.kwargs['dept']
        return course_models.Course.objects.filter(dept=dept)


class CourseDetailView(generics.RetrieveAPIView):
    """Retrieve all of the sections ever offered by a course."""
    serializer_class = course_serializers.CourseSerializer

    def get_object(self):
        fields_to_match = {
            'dept': self.kwargs['dept'],
            'course_num': self.kwargs['course_num']
        }

        return course_models.Course.objects.get(**fields_to_match)


class SectionView(generics.GenericAPIView):
    """Lists all sections of a course matching filtering criteria.
    Use the following query parameters to filter results.

    - `semester`: (`fall`, `summer`, `spring`)
    - `campus`: (`cs`, `gv`, `qt`)
    - `year`: (`2009` onwards)

    Providing all three query parameters will send back one specific result, not a list of results.
    """
    serializer_class = course_serializers.SectionSerializer
    field_options = {
        'semester': {
            'spring': '1',
            'summer': '2',
            'fall': '3'
        },
        'campus': {
            'cs': '1',
            'gv': '2',
            'qt': '3'
        },
        'year': list(map(str, range(2009, datetime.date.today().year + 1)))
    }

    def get_queryset(self):
        dept = self.kwargs['dept']
        course_num = self.kwargs['course_num']
        section_num = self.kwargs['section_num']
        course = shortcuts.get_object_or_404(
            course_models.Course.objects.all(), dept=dept, course_num=course_num)
        return course_models.Section.objects.filter(course=course, section_num=section_num)

    def is_invalid_value(self, value, allowed_values):
        return value not in allowed_values

    def validated_filter_fields(self):
        """Checks the values of the query parameters against the allowed values.
        
        Returns:
            A dict of validated query parameters, or Http400BadResponse if any of the values aren't valid.
        """
        query_params = self.request.query_params
        for key in query_params:
            if key not in self.field_options:
                continue
            if self.is_invalid_value(query_params[key], self.field_options[key]):
                return None, http_response.HttpResponseBadRequest()
        return query_params, None

    def construct_term_codes_from_fields(self, fields):
        """Given a combination of fields to filter on, construct a term code.

        Args:
            fields: A dictionary of fields whose keys are some combination of "semester", "campus", and "year"
        Returns:
            A list of term codes matching the filtering criteria.
        """
        years = self.field_options['year']
        if 'year' in fields:
            years = [str(fields['year'])]

        semesters = self.field_options['semester'].values()
        if 'semester' in fields:
            semester_option = fields['semester']
            semesters = [self.field_options['semester'][semester_option]]

        campuses = self.field_options['campus'].values()
        if 'campus' in fields:
            campus_option = fields['campus']
            campuses = [self.field_options['campus'][campus_option]]

        term_codes = []
        for year in years:
            for semester in semesters:
                for campus in campuses:
                    term_codes.append(year+semester+campus)
        return term_codes

    def get(self, *args, **kwargs):
        filter_fields, bad_response = self.validated_filter_fields()
        if bad_response:
            return bad_response
        term_codes = self.construct_term_codes_from_fields(filter_fields)
        serializer = self.serializer_class
        if len(term_codes) == 1:
            obj = shortcuts.get_object_or_404(
                self.get_queryset(), term_code=term_codes[0])
            return response.Response(serializer(obj).data)
        else:
            objs = self.get_queryset().filter(term_code__in=term_codes).all()
            return response.Response(serializer(objs, many=True).data)
