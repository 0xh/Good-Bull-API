from rest_framework import serializers
from goodbullapi.models import GPADistribution


class GPADistributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GPADistribution
        fields = ('ABCDFQ',)