from rest_framework import serializers
from goodbullapi.models import GPADistribution, Instructor


class GPADistributionSerializer(serializers.ModelSerializer):
    gpa = serializers.FloatField(read_only=True)
    instructor = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    dept = serializers.CharField(source='section.dept')
    course_num = serializers.CharField(source='section.course_num')
    section_num = serializers.CharField(source='section.section_num')
    term_code = serializers.CharField(source='section.term_code')

    class Meta:
        model = GPADistribution
        fields = ('ABCDFQ', 'gpa', 'instructor', 'dept', 'course_num', 'section_num', 'term_code')
        read_only = ('dept', 'course_num', 'section_num', 'term_code')


class InstructorSerializer(serializers.ModelSerializer):
    sections_taught = GPADistributionSerializer(many=True, read_only=True)

    class Meta:
        model = Instructor
        fields = ('name', 'sections_taught')

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related('sections_taught')
        return queryset
