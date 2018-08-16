import graphene
from graphene_django import filter as gd_filter
from graphene_django import types as graphene_types

from courses import models as course_models
from sections import models as section_models
from shared import schema_options as shared_schema_options


class MeetingType(graphene_types.DjangoObjectType):
    meeting_type = graphene.String()

    class Meta:
        model = section_models.Meeting


class SectionNode(graphene_types.DjangoObjectType):
    meetings = graphene.List(MeetingType)

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
    section = graphene.Field(SectionNode,
                             _id=graphene.String(),
                             crn=graphene.Int(),
                             dept=graphene.String(),
                             course_num=graphene.String(),
                             section_num=graphene.String(),
                             term_code=graphene.Int())
    sections = gd_filter.DjangoFilterConnectionField(SectionNode)

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
