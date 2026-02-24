from ariadne import gql, QueryType, make_executable_schema, MutationType, snake_case_fallback_resolvers
from ariadne.asgi import GraphQL

from datetime import datetime

from core.infrastructure.models import Order

query = QueryType()
mutation = MutationType()

type_defs = gql("""
    input OrderItemInput {
        id: ID!
        title: String!
        author: String!
        createdAt: String!
    }

    input CreateOrderInput {
        item: OrderItemInput
    }

    type Order {
        id: ID!
        title: String!
        author: String!
        createdAt: String!
    }

    type Mutation {
        createOrder(data: CreateOrderInput!): Order!
    }

    type Balance {
        id: ID!
        balance: Int!
    }

    input BalanceInput {
        id: Int!
    }

    type Query {
        balance(input: BalanceInput): Balance!
    }
""")

@query.field("balance")
def resolve_balance(*_):
    pass


@mutation.field("createOrder")
def resolve_create_mutation(obj, info, data):
    print(f"Данные с frontend: {data}")
    now = datetime.now()
    order = Order.objects.create(title=data['item']["title"], author="Jack", created_at=now)
    print("Success in creating order")
    return order

    

schema = make_executable_schema(type_defs, query, mutation, snake_case_fallback_resolvers)
app = GraphQL(schema, debug=True)