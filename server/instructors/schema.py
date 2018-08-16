import graphene
from graphene_django import types as graphene_types

from instructors import models as instructor_models
from shared import schema_options as shared_schema_options


class InstructorType(graphene_types.DjangoObjectType):
    class Meta:
        model = instructor_models.Instructor
        filter_fields = {
            'name': shared_schema_options.STRING_FILTER_OPTIONS
        }
        interfaces = (graphene.relay.Node,)


class Query(object):
    all_instructors = graphene.List(InstructorType)
    instructor = graphene.Field(InstructorType, name=graphene.String())

    def resolve_all_instructors(self, info, **kwargs):
        return instructor_models.Instructor.objects.all()

    def resolve_instructor(self, info, **kwargs):
        name = kwargs.get('name')

        if name is not None:
            return instructor_models.Instructor.objects.get(name=name)
        return None
