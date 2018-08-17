import graphene
from graphene_django import filter as gd_filter
from graphene_django import types as graphene_types

from courses import models as course_models
from shared import schema_options as shared_schema_options


class Course(graphene_types.DjangoObjectType):
    """A representation of a course taught at Texas A&M University from term to term."""
    class Meta:
        model = course_models.Course
        filter_fields = {
            'dept': shared_schema_options.STRING_FILTER_OPTIONS,
            'course_num': shared_schema_options.STRING_FILTER_OPTIONS,
            'name': shared_schema_options.STRING_FILTER_OPTIONS,
            'min_credits': shared_schema_options.NUMERIC_FILTER_OPTIONS,
            'max_credits': shared_schema_options.NUMERIC_FILTER_OPTIONS,
            'description': shared_schema_options.STRING_FILTER_OPTIONS,
            'prereqs': shared_schema_options.STRING_FILTER_OPTIONS,
            'coreqs': shared_schema_options.STRING_FILTER_OPTIONS
        }
        interfaces = (graphene.relay.Node,)


class Query(object):
    course = graphene.relay.Node.Field(Course)
    courses = gd_filter.DjangoFilterConnectionField(Course)

    def resolve_courses(self, info, **kwargs):
        return course_models.Course.objects.all()

    def resolve_course(self, info, **kwargs):
        _id = kwargs.get('_id')
        if _id is not None:
            return course_models.Course.objects.get(_id=_id)

        dept = kwargs.get('dept')
        course_num = kwargs.get('course_num')
        if dept is not None and course_num is not None:
            return course_models.Course.objects.get(dept=dept, course_num=course_num)

        return None
