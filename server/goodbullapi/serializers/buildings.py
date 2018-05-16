from rest_framework import serializers
from goodbullapi.models import Building

class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = ('abbr', 'name', 'address', 'city', 'zip_code')