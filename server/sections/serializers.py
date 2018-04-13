from rest_framework import serializers
from sections.models import Section, Meeting

class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = ('meeting_type', 'start_time', 'end_time', 'days')

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ('_id', 'crn', 'section', 'honors', 'name', 'meetings')
