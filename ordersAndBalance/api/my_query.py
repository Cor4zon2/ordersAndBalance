from ariadne import gql, QueryType, MutationType, make_executable_schema

# asgi?
from ariadne.asgi import GraphQL


query = QueryType()
mutation = MutationType()

type_defs = gql("""
    # type Query {
    #     # orders: [Order]
    #     hello: String!
    # }

    type Query {
        orders: [Order!]!
    }

    type Order {
        title: String
        client: Int!
        price: Int!
    }

    type OrdersList {
        orders: [Order!]!
    }


    input CreateOrderInput {
        title: String
        client: Int!
        price: Int!
    }

    type Mutation {
        create_order(input: CreateOrderInput): Order!
    }
""")


# why? *_
# it means throw away all parameters
# @query.field("hello")
# def resolve_hello(*_):
#     return 'Boooo!'

# @query.field("title")
def resolve_balance(*_):
    return 'my balance'


@query.field("orders")
def resolve_orders(*_):
    return [
        {"title": "Bilbo Baggins", "client": 120, "price": 3209},
        {"title": "Boris Britva", "client": 10, "price": 1100000}
    ]

@mutation.field("create_order")
def resolve_create_order(_, info):
    return {"title": "Bom", "client": 1, "price": 0}

# binding to schema
schema = make_executable_schema(type_defs, [query, mutation])

# app = GraphQL(schema, debug=True)