from ariadne import gql, QueryType, make_executable_schema, MutationType, snake_case_fallback_resolvers
from ariadne.asgi import GraphQL

from core.infrastructure.models import Order
from core.domain.domain import create_order, get_order_by_id

query = QueryType()
mutation = MutationType()

type_defs = gql("""
    type OrderItem {
        id: ID!
        name: String
        amount: Int!
    }

    enum OrderStatus {
        PENDING
        PAID
        CANCELED
    }

    type Order {
        id: ID!
        items: [OrderItem!]!
        # потенциальная ошибка
        price: Int!
        clientId: ID!
        status: OrderStatus!
    }

    input OrderItemInput {
        id: ID!
        amount: Int!
    }
    
    input CreateOrderInputs {
        clientId: ID!
        items: [OrderItemInput!]!
    }

    type Mutation {
        createOrder(inputs: CreateOrderInputs): Order!
    }

    input GetOrderInputs {
        id: ID!
    }

    type Query {
        getOrder(inputs: GetOrderInputs): Order!
    }
""")



@mutation.field("createOrder")
def resolve_create_mutation(obj, info, inputs):
    items = inputs["items"]
    clientId = inputs["clientId"]

    order = {
        "clientId": clientId,
        "items": items,
    }
    new_order = create_order(order)

    return new_order


@query.field("getOrder") 
def resolve_get_order(obj, info, inputs):
    id = inputs["id"]
    order = get_order_by_id(id)
    return order

schema = make_executable_schema(type_defs, query, mutation, snake_case_fallback_resolvers)
app = GraphQL(schema, debug=True)