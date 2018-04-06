from rest_framework import serializers
from courses.models import Course

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('_id', 'name', 'description', 'division_of_hours', 'prereqs')
