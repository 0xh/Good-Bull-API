import graphene

import buildings.schema
import courses.schema
import instructors.schema
import sections.schema


class Query(buildings.schema.Query,
            courses.schema.Query,
            instructors.schema.Query,
            sections.schema.Query,
            graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
