import graphene
from graphene import relay, ObjectType, AbstractType, List, String, Field, Int, Boolean
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import Product
from orgs.models import Org
from orgs.schema import OrgNode
from graphql_relay.node.node import from_global_id
from django.core.exceptions import ObjectDoesNotExist

##############################################################################################

#                 RETRIEVE and FILTER

##############################################################################################

class ProductNode(DjangoObjectType):
    class Meta:
        model = Product
        filter_fields = {
            'id': ['exact'],
            'name': ['exact', 'icontains', 'istartswith'],
            'org__name': ['icontains'],
            'org__admin__username':['icontains'],
        }
        interfaces = (relay.Node, )
    # @classmethod
    # def get_node(cls, id, context, info):
    #     return Product.objects.get(id = id)


##############################################################################################

#                 CREATE or UPDATE

##############################################################################################

class ProductInput(graphene.InputObjectType):
    product_id  = String()
    name = String(required=True)
    org_id = String(required=True)
    description = String()

class SaveProduct(relay.ClientIDMutation):
    '''
        TODO: Django bulk create
    '''
    class Input:
        product_data = graphene.Argument(ProductInput)

    product = Field(ProductNode)
    org = Field(OrgNode)
    updated = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        product_data = input.get('product_data')
        name = product_data.get('name')
        org = Org.objects.get(pk = product_data.get('org_id'))
        description = product_data.get('description')
        product_id = product_data.get('product_id')
        print('context: ' + str(context))
        if product_id:
            id = from_global_id(product_id)[1]
            product = Product.objects.get(pk=id)
            product.name = name
            product.org = org
            product.description = description
            product.save()
            updated = True

        else:
            product = Product.objects.create(name = name, org = org, description = description, order_price = 12.6, sell_price = 20)
            updated = False

        return SaveProduct(product = product, org = org, updated = updated)


##############################################################################################

#                 DELETE

##############################################################################################

class DeleteProduct(relay.ClientIDMutation):
    '''
        TODO: Delete multiple objects from a list of ID's
        Product.objects.filter(id__in=(1,2)).delete()
    '''
    class Input:
        product_id  = String(required=True)


    product = Field(ProductNode)
    delete_count = Int()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        node_id = input.get('product_id')
        id = from_global_id(node_id)[1]
        product = Product.objects.get(pk=id)
        count, list = product.delete()
        return DeleteProduct(delete_count = count, product = product)


##############################################################################################

#                 DECLARATIONS

##############################################################################################

class Query(object):
    all_products = DjangoFilterConnectionField(ProductNode)

    # def resolve_all_products(self, args, context, info):
    #     return Product.objects.all()

class Mutation(object):
    save_product = SaveProduct.Field()
    delete_product = DeleteProduct.Field()
