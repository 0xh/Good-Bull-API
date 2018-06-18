from rest_framework import viewsets
from goodbullapi.models import Building
from goodbullapi.serializers import BuildingSerializer


class BuildingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
