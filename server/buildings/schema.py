import graphene
from graphene_django import filter as gd_filter
from graphene_django import types as graphene_types

from buildings import models as building_models
from shared import schema_options as shared_schema_options


class BuildingNode(graphene_types.DjangoObjectType):
    class Meta:
        model = building_models.Building
        filter_fields = {
            'abbr': ['exact'],
            'address': shared_schema_options.STRING_FILTER_OPTIONS,
            'city': shared_schema_options.STRING_FILTER_OPTIONS,
            'location_description': shared_schema_options.STRING_FILTER_OPTIONS,
            'name': shared_schema_options.STRING_FILTER_OPTIONS,
            'num_floors': shared_schema_options.NUMERIC_FILTER_OPTIONS,
            'year_built': shared_schema_options.NUMERIC_FILTER_OPTIONS,
            'zip_code': ['exact']
        }
        interfaces = (graphene.relay.Node,)


class Query(object):
    building = graphene.relay.Node.Field(BuildingNode)
    buildings = gd_filter.DjangoFilterConnectionField(BuildingNode)

    def resolve_buildings(self, info, **kwargs):
        return building_models.Building.objects.all()

    def resolve_building(self, info, **kwargs):
        abbr = kwargs.get('abbr')
        name = kwargs.get('name')

        if abbr is not None:
            return building_models.Building.objects.get(abbr=abbr)

        if name is not None:
            return building_models.Building.objects.get(name=name)

        return None
