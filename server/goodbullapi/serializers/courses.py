from rest_framework import serializers
from goodbullapi.models import Course
from .sections import SectionSerializer


class CourseSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = (
            'dept',
            'course_num',
            'term_code',
            'least_credits',
            'most_credits',
            'name',
            'description',
            'division_of_hours',
            'prereqs',
            'sections'
        )
    
    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related('sections')
        return queryset