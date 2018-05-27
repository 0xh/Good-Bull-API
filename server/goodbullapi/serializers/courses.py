from rest_framework import serializers
from goodbullapi.models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('dept', 'course_num', 'name', 'distribution_of_hours',
                  'description', 'prereqs', 'coreqs', 'min_credits', 'max_credits')
