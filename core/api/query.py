from ariadne import gql, QueryType, make_executable_schema, MutationType, snake_case_fallback_resolvers
from ariadne.asgi import GraphQL

from core.infrastructure.models import Order, Refund
from core.domain.domain import create_order, get_order_by_id

query = QueryType()
mutation = MutationType()

type_defs = gql("""
    enum OrderStatus {
        PENDING
        PAID
        CANCELED
    }

    type Order {
        id: ID!
        idempotencyKey: String!
        userId: ID!
        totalPrice: Int!
        createdAt: String!
        status: OrderStatus!
        items: [OrderProducts!]!
    }

    type OrderProducts {
        id: ID!
        product: Product!
        productPriceFreezed: Int!
        quantity: Int!
    }

    type Product {
        id: ID!
        name: String!
        price: Int!
    }

    type User {
        id: ID!
        name: String!
        email: String!
        wallet: Wallet!
    }

    type Wallet {
        id: ID!
        userId: ID!
        balance: Int!
    }

    type Refund {
        id: ID!
        idempotencyKey: String!
        orderId: ID!
        reason: String!
        createdAt: String!
    }

    type SuccessOrderCreation {
        success: Boolean!
    }

    type ErrorUnknown {
        title: String!
        message: String!
    }

    type ErrorBalance {
        title: String!
        message: String!
    }

    # mutation

    union CreateOrderResults = SuccessOrderCreation | ErrorUnknown | ErrorBalance

    input OrderItemInput {
        productId: ID!
        quantity: Int!
    }

    input CreateOrderInputs {
        userId: ID!
        idempotencyKey: String!
        items: [OrderItemInput!]!
    }

    type SuccessRefundCreation {
        success: Boolean!
    }

    union CreateRefundResults = SuccessRefundCreation | ErrorUnknown

    input CreateRefundInputs {
        orderId: ID!
        userId: ID!
        reason: String!
        idempotencyKey: String!
    }

    type Mutation {
        createOrder(input: CreateOrderInputs!): CreateOrderResults!
        createRefund(input: CreateRefundInputs!): CreateRefundResults!
    }


    # query

    input GetUserInputs {
        userId: ID!
    }


    type SuccessfullyGetUser {
        user: User!
    }

    type ErrorAuth {
        title: String!
        message: String!
    }

    union GetUserResult = SuccessfullyGetUser | ErrorAuth

    input GetOrderListInputs {
        userId: ID!
        lastId: ID
        orderStatus: OrderStatus
    }

    type GetOrdersListResult {
        orders: [Order!]!
    }

    input GetProductListInputs {
        lastId: ID
    }

    type GetProductListResult {
        products: [Product!]!
    }

    type Query {
        getUser(input: GetUserInputs): GetUserResult!
        getOrdersList(input: GetOrderListInputs!): GetOrdersListResult!
        getProductList(input: GetProductListInputs!): GetProductListResult!
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
    refunds = Refund.objects.select_related("order").all()

    return {"refunds": refunds}

schema = make_executable_schema(type_defs, query, mutation, snake_case_fallback_resolvers, mock=True)
app = GraphQL(schema, debug=True)