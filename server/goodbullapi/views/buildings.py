from goodbullapi.models import Building
from goodbullapi.serializers import BuildingSerializer
from rest_framework import viewsets

class BuildingViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BuildingSerializer
    queryset = Building.objects.all()
