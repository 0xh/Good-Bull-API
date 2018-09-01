from rest_framework import serializers

from courses import models as course_models


class FilteredListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        if 'term_code' in self.context:
            term_code = self.context['term_code']
            data = data.filter(term_code=term_code)
        return super(FilteredListSerializer, self).to_representation(data)


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = course_models.Meeting
        fields = ('location', 'meeting_days', 'start_time',
                  'end_time', 'meeting_type',)


class GradeDistributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = course_models.GradeDistribution
        fields = ('ABCDFISUQX', 'gpa')


class SectionSerializer(serializers.ModelSerializer):
    meetings = MeetingSerializer(many=True, read_only=True)
    grade_distribution = GradeDistributionSerializer(read_only=True)
    instructor = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        list_serializer_class = FilteredListSerializer
        model = course_models.Section
        fields = ('name', 'crn', 'section_num', 'term_code',
                  'instructor', 'meetings', 'grade_distribution')


class CourseSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, read_only=True)

    class Meta:
        model = course_models.Course
        fields = ('dept', 'course_num', 'name', 'distribution_of_hours',
                  'prereqs', 'coreqs', 'min_credits', 'max_credits', 'sections')


class CourseOverviewSerializer(CourseSerializer):

    class Meta:
        model = course_models.Course
        fields = ('dept', 'course_num', 'name', 'distribution_of_hours',
                  'prereqs', 'coreqs', 'min_credits', 'max_credits')
