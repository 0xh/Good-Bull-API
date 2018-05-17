from rest_framework import generics
from goodbullapi.models import Instructor
from goodbullapi.serializers import InstructorSerializer
from django.shortcuts import get_object_or_404


class InstructorRetrieve(generics.RetrieveAPIView):
    serializer_class = InstructorSerializer
    queryset = Instructor.objects.all()