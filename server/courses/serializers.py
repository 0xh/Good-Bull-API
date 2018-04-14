from rest_framework import serializers
from courses.models import Course
from sections.serializers import SectionSerializer


class CourseSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = (
            '_id',
            'short',
            'term_code',
            'name',
            'description',
            'division_of_hours',
            'prereqs',
            'sections'
        )
