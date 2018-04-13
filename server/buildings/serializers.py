from rest_framework import serializers
from buildings.models import Building


class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = ('abbr', 'name', 'address', 'city', 'zip_code')
