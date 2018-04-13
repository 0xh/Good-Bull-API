from django.shortcuts import render
from rest_framework import viewsets
from sections.models import Section
from sections.serializers import SectionSerializer

# Create your views here.
class SectionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

