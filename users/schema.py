import graphene
from graphene import relay, ObjectType, AbstractType, List, String, Field, Int, Boolean
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from django.contrib.auth import authenticate
from users.models import User

def get_user(context):
    token = context.session.get('token')
    if not token:
        return
    try:
        user = User.objects.get(token=token)
        return user
    except:
        raise Exception('User not found!')


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = {
            'id': ['exact'],
        }
        interfaces = (graphene.relay.Node, )


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserNode)

    class Input:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    @staticmethod
    def mutate(self, info, username, password, email):
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()

        return CreateUser(user=user)

class LogIn(graphene.Mutation):
    user = graphene.Field(UserNode)

    class Input:
        username = graphene.String()
        password = graphene.String()

    @staticmethod
    def mutate(self, info, username, password):
        user = authenticate(username=username, password=password)

        if not user:
            raise Exception('Invalid username or password!')

        info.context.session['token'] = user.token
        return LogIn(user=user)

class LogOut(graphene.Mutation):
    user = graphene.Field(UserNode)

    @staticmethod
    def mutate(self, info):
        user = get_user(info.context)
        info.context.session['token'] = None

        return LogOut(user=user)


class Query(object):
    all_users = DjangoFilterConnectionField(UserNode)
    viewer = graphene.Field(UserNode)

    def resolve_viewer(self, info):
        user = get_user(info.context)

        if not user:
            raise Exception('Not logged!')
        return user

class Mutation(object):
    create_user = CreateUser.Field()
    login = LogIn.Field()
    logout = LogOut.Field()
