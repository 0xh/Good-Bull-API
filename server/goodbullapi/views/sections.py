from goodbullapi.models import Section
from goodbullapi.serializers import SectionSerializer
from rest_framework import viewsets

class SectionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SectionSerializer
    queryset = Section.objects.all()
