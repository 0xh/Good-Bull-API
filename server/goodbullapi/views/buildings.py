from goodbullapi.models import Building
from goodbullapi.serializers import BuildingSerializer
from rest_framework import viewsets

class BuildingViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Provides `list` and `retrieve` functionality for all buildings.
    """
    serializer_class = BuildingSerializer
    queryset = Building.objects.all()
