from rest_framework import serializers
from goodbullapi.models import Section, Meeting
from .instructors import GPADistributionSerializer

class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = ('meeting_type', 'start_time', 'end_time', 'days')


class SectionSerializer(serializers.ModelSerializer):
    meetings = MeetingSerializer(many=True, read_only=True)
    gpa_distribution = GPADistributionSerializer(many=False, read_only=True)
    class Meta:
        model = Section
        fields = (
            'crn',
            'term_code',
            'dept',
            'course_num',
            'section_num',
            'honors',
            'section_name',
            'meetings',
            'least_credits',
            'most_credits',
            'gpa_distribution')
