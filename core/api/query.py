from ariadne import gql, QueryType, make_executable_schema, MutationType, snake_case_fallback_resolvers
from ariadne.asgi import GraphQL

from core.infrastructure.models import Order

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

@query.field("balance")
def resolve_balance(*_):
    pass


@mutation.field("createOrder")
def resolve_create_mutation(obj, info, data):
    print(f"Данные с frontend: {data}")
    order = Order.objects.create(title=data['item']["title"], author=data['item']["author"], created_at=data['item']["createdAt"])
    print("Success in creating order")
    return order


@query.field("order") 
def resolve_order(obj, info, input):
    print("Пошли")
    order = Order.objects.get(id=input["id"])
    print("Нашли")
    return order

schema = make_executable_schema(type_defs, query, mutation, snake_case_fallback_resolvers)
app = GraphQL(schema, debug=True)