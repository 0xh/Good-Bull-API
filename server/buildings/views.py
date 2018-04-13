from django.shortcuts import render
from rest_framework import viewsets
from buildings.models import Building
from buildings.serializers import BuildingSerializer

# Create your views here.


class BuildingViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    This is all that should be required when it comes to accessing building data.
    """
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
