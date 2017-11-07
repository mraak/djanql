import graphene
from graphene import relay, ObjectType, AbstractType, List, String, Field, Int, Boolean
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import Org
from django.contrib.auth.models import User
from graphql_relay.node.node import from_global_id
from django.core.exceptions import ObjectDoesNotExist

##############################################################################################

#                 RETRIEVE and FILTER

##############################################################################################



class OrgNode(DjangoObjectType):
    class Meta:
        model = Org
        filter_fields = {
            'id': ['exact'],
        }
        interfaces = (graphene.relay.Node, )
    # @classmethod
    # def get_node(cls, id, context, info):
    #     return Org.objects.get(id = id)

##############################################################################################

#                 CREATE or UPDATE

##############################################################################################

class OrgInput(graphene.InputObjectType):
    org_id = String()
    admin_id = String(required=True)
    name = String(required=True)

class SaveOrg(relay.ClientIDMutation):
    class Input:
        org_data = graphene.Argument(OrgInput)

    org = Field(OrgNode)
    updated = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, org_data):
        org_id = org_data.get('org_id')
        admin_id = org_data.get('admin_id')
        name = org_data.get('name')
        if org_id:
            id = from_global_id(org_id)[1]
            org = Org.objects.get(pk=id)
            org.name = name
            org.admin_id = from_global_id(admin_id)[1]
            org.save()
            updated = True
        else:
            org = Org.objects.create(name = name, admin_id = from_global_id(admin_id)[1])
            updated = False

        return SaveOrg(org = org, updated = updated)


##############################################################################################

#                 DELETE

##############################################################################################

class DeleteOrg(relay.ClientIDMutation):
    class Input:
        org_id = graphene.String()

    org = Field(OrgNode)
    delete_count = Int()

    @classmethod
    def mutate_and_get_payload(cls, root, info, org_id):
        id = from_global_id(org_id)[1]
        org = Org.objects.get(pk=id)
        count, list = product.delete()



##############################################################################################

#                 DECLARATIONS

##############################################################################################


class Query(object):
    all_orgs = DjangoFilterConnectionField(OrgNode)
    org = relay.Node.Field(OrgNode)

    # def resolve_viewer(self, args, context, info):
    #     print ("resolve_viewer", args, context)
    #     id = args.get('id')
    #     return User.objects.get(pk=id)
    #
    # def resolve_org(self, args, context, info):
    #     print ("resolve_org", args, context)
    #     return Org.objects.get(pk=1)
    #
    # def resolve_all_orgs(self, args, context, info):
    #     print ("resolve_all_orgs", args, context)
    #     return Org.objects.all()


class Mutation(object):
    save_org = SaveOrg.Field()
