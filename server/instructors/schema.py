import graphene
from graphene_django import types as graphene_types

from instructors import models as instructor_models
from shared import schema_options as shared_schema_options


class Instructor(graphene_types.DjangoObjectType):
    """An instructor who has (at one point) taught at Texas A&M University."""
    class Meta:
        model = instructor_models.Instructor
        filter_fields = {
            'name': shared_schema_options.STRING_FILTER_OPTIONS
        }
        interfaces = (graphene.relay.Node,)


class Query(object):
    instructors = graphene.List(Instructor)
    instructor = graphene.Field(Instructor, name=graphene.String())

    def resolve_instructors(self, info, **kwargs):
        return instructor_models.Instructor.objects.all()

    def resolve_instructor(self, info, **kwargs):
        name = kwargs.get('name')

        if name is not None:
            return instructor_models.Instructor.objects.get(name=name)
        return None
