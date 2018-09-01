from rest_framework import generics
from instructors import serializers as instructor_serializers
from instructors import models as instructor_models


class InstructorRetrieveView(generics.RetrieveAPIView):
    serializer_class = instructor_serializers.InstructorSerializer
    queryset = instructor_models.Instructor.objects