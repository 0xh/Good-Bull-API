import graphene
from graphene_django import filter as gd_filter
from graphene_django import types as graphene_types

from courses import models as course_models
from sections import models as section_models
from shared import schema_options as shared_schema_options

# https://stackoverflow.com/questions/46407277/enforce-pagination-in-graphene-relay-connectionfield

DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100


class Meeting(graphene_types.DjangoObjectType):
    """A time at which a Section meets."""
    meeting_type = graphene.String()

    class Meta:
        model = section_models.Meeting


class GradeDistribution(graphene_types.DjangoObjectType):
    """The grades achieved by students in a certain Section."""
    class Meta:
        model = section_models.GradeDistribution


class Section(graphene_types.DjangoObjectType):
    """A specific group of students taking a Course 
    that meet at scheduled times during the week."""
    meetings = graphene.List(Meeting)

    def resolve_meetings(self, info, **kwargs):
        return self.meetings.all()

    class Meta:
        model = section_models.Section
        filter_fields = {
            'crn': ['exact'],
            'name': shared_schema_options.EXACT_AND_CONTAINING_OPTIONS,
            'section_num': shared_schema_options.EXACT_AND_CONTAINING_OPTIONS,
            'term_code': ['exact']
        }
        interfaces = (graphene.relay.Node,)


class Query(object):
    section = graphene.Field(Section,
                             _id=graphene.String(),
                             crn=graphene.Int(),
                             dept=graphene.String(),
                             course_num=graphene.String(),
                             section_num=graphene.String(),
                             term_code=graphene.Int())
    sections = gd_filter.DjangoFilterConnectionField(Section)

    def resolve_section(self, info, **kwargs):
        # Lookup by ID
        _id = kwargs.get('_id')
        if _id is not None:
            return section_models.Section.objects.get(_id=_id)

        # Lookup by crn + term_code (unique together)
        crn = kwargs.get('crn')
        term_code = kwargs.get('term_code')
        if crn is not None and term_code is not None:
            return section_models.Section.objects.get(crn=crn, term_code=term_code)

        # Lookup by course relation + section_num + term_code (unique together)
        dept = kwargs.get('dept')
        course_num = kwargs.get('course_num')
        section_num = kwargs.get('section_num')
        if dept is not None and course_num is not None:
            course = course_models.Course.objects.get(
                dept=dept, course_num=course_num)
            if section_num is not None and term_code is not None:
                return section_models.Section.objects.get(course=course, section_num=section_num, term_code=term_code)
        return None

    def resolve_sections(self, info, **kwargs):
        return section_models.Section.objects.all()
