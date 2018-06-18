from rest_framework import serializers

from goodbullapi.models import Building


class BuildingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Building
        fields = ('abbr', 'name', 'location_description', 'year_built',
                  'num_floors', 'address', 'city', 'zip_code', 'search_vector')
