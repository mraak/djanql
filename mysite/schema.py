import graphene

import products.schema
import orgs.schema
import courses.schema
import users.schema

class Query(products.schema.Query, orgs.schema.Query, users.schema.Query, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass
#
class Mutation(products.schema.Mutation, orgs.schema.Mutation, users.schema.Mutation, graphene.ObjectType):
    pass

# schema = graphene.Schema(query = courses.schema.Query, mutation = courses.schema.Mutation)
schema = graphene.Schema(query=Query, mutation=Mutation)
