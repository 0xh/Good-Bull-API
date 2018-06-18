from rest_framework import serializers
from goodbullapi.models import Instructor


class InstructorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Instructor
        fields = ('name',)