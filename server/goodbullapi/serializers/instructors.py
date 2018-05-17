from rest_framework import serializers
from goodbullapi.models import GPADistribution, Instructor


class GPADistributionSerializer(serializers.ModelSerializer):
    gpa = serializers.FloatField(read_only=True)
    class Meta:
        model = GPADistribution
        fields = ('ABCDFQ', 'gpa')

class InstructorSerializer(serializers.ModelSerializer):
    sections_taught = GPADistributionSerializer(many=True, read_only=True)

    class Meta:
        model = Instructor
        fields = ('name', 'sections_taught')
