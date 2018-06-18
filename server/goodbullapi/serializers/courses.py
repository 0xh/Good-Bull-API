from rest_framework import serializers
from goodbullapi.models import Course
from .sections import SectionSerializer

class CourseSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, read_only=True)
    class Meta:
        model = Course
        fields = ('dept', 'course_num', 'name', 'distribution_of_hours',
                  'description', 'prereqs', 'coreqs', 'min_credits', 'max_credits', 'sections')
