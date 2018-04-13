from rest_framework import serializers
from courses.models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = (
            '_id',
            'short',
            'term_code',
            'name',
            'description',
            'division_of_hours',
            'prereqs')
