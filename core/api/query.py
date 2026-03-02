from ariadne import gql, QueryType, make_executable_schema, MutationType, snake_case_fallback_resolvers
from ariadne.asgi import GraphQL

from core.infrastructure.models import Order, Refund
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

    union CreateRefundResult = SuccessfullyCreatedRefund | ErrorUnknown

    type SuccessfullyCreatedRefund {
        _: Boolean
    }

    type ErrorUnknown {
        title: String!
        errorCode: String
    }

    input CreateRefundInput {
        reason: String!
        orderId: ID!
    }

    type Mutation {
        createOrder(inputs: CreateOrderInputs): Order!
        createRefund(inputs: CreateRefundInput): CreateRefundResult!
    }

    input GetOrderInputs {
        id: ID!
    }

    type RefundType {
        id: ID!
        orderId: ID!
        reason: String!
        createdAt: String!
    }

    type RefundsList {
        refunds: [RefundType!]!
    }

    type Query {
        getOrder(inputs: GetOrderInputs): Order!
        getRefundsList: RefundsList!
    }
""")

import logging
logger = logging.getLogger(__name__)
logger.error("Это должно быть видно везде!")

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


@query.field("getRefundsList")
def resolve_get_refunds(obj, info):
    refunds = Refund.objects.all()

    for refund in refunds:
        print(refund.order.title)

    return refunds

schema = make_executable_schema(type_defs, query, mutation, snake_case_fallback_resolvers)
app = GraphQL(schema, debug=True)