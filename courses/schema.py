import graphene
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import Course


class CourseNode(DjangoObjectType):
    class Meta:
        model = Course
        interfaces = (graphene.relay.Node, )

class CreateCourse(graphene.relay.ClientIDMutation):
    class Input:
        name = graphene.String(required=True)

    course = graphene.Field(CourseNode)

    @classmethod
    def mutate_and_get_payload(cls, input, args, info):
        name = input.get('name')
        c = Course.objects.create(name = name)
        course = CourseNode(c)
        return CreateCourse(course = course)


class Query(graphene.ObjectType):
    all_courses = DjangoFilterConnectionField(CourseNode)

    def resolve_all_courses(self, args, context, info):
        return Course.objects.all()

class Mutation(graphene.ObjectType):
    create_course = CreateCourse.Field()
