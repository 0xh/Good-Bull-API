from rest_framework import serializers

from courses import serializers as course_serializers
from instructors import models as instructor_models


class InstructorSerializer(serializers.ModelSerializer):
    distributions = serializers.SerializerMethodField()

    class Meta:
        model = instructor_models.Instructor
        fields = ('name', 'distributions')

    def get_distributions(self, obj):
        grouped_distributions = {}
        sections_taught = obj.sections_taught
        sections_taught = sections_taught.prefetch_related(
            'course').select_related('grade_distribution')
        for section in sections_taught.all():
            dept_course = section.course.pk
            if dept_course not in grouped_distributions:
                grouped_distributions[dept_course] = []
            if section.grade_distribution:
                grouped_distributions[dept_course].append(
                    section.grade_distribution)
        for key in grouped_distributions:
            grouped_distributions[key] = course_serializers.GradeDistributionSerializer(
                grouped_distributions[key], many=True).data
        return grouped_distributions
