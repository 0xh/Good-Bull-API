from rest_framework import serializers

from goodbullapi.models import Instructor, Meeting, Section

from .instructors import InstructorSerializer


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = ('location', 'meeting_days',
                  'start_time', 'end_time', 'meeting_type')


class SectionSerializer(serializers.ModelSerializer):
    """Serializes a Section."""
    meetings = MeetingSerializer(many=True, read_only=True)
    instructor = InstructorSerializer(read_only=True)

    class Meta:
        model = Section
        fields = ('name', 'crn', 'section_num',
                  'term_code', 'instructor', 'meetings')
