from ariadne import gql, QueryType, make_executable_schema, MutationType, snake_case_fallback_resolvers, UnionType
from ariadne.asgi import GraphQL

from core.infrastructure.models import Order, Refund
from core.domain.domain import create_order, get_order_by_id

from datetime import datetime

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

    type Payment {
        id: ID!
        idempotencyKey: String!
        wallet: Wallet!
        order: Order!
        price: Int!
        createdAt: String!
        status: OrderStatus!
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

    type SuccessPaymentCreation {
        success: Boolean!
    }

    union CreatePaymentResult = SuccessPaymentCreation | ErrorUnknown

    input CreatePaymentInput {
        idempotencyKey: String!
        orderId: ID!
        walletId: ID!
    }

    type Mutation {
        createOrder(input: CreateOrderInputs!): CreateOrderResults!
        createRefund(input: CreateRefundInputs!): CreateRefundResults!
        createPayment(input: CreatePaymentInput!): CreatePaymentResult!
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

    input GetPaymentsListInput {
        userId: ID!
        lastId: ID
    }

    type GetPaymentListResult {
        payments: [Payment!]!
        lastId: ID!
    }

    type Query {
        getUser(input: GetUserInputs): GetUserResult!
        getOrdersList(input: GetOrderListInputs!): GetOrdersListResult!
        getProductList(input: GetProductListInputs!): GetProductListResult!
        getPaymentsList(input: GetPaymentsListInput!): GetPaymentListResult!
    }
""")

import logging
logger = logging.getLogger(__name__)
# logger.error("Это должно быть видно везде!")

@mutation.field("createOrder")
def resolve_create_order(obj, info, inputs):
    items = inputs["items"]
    userId = inputs["userId"]

    order = {
        "userId": userId,
        "items": items,
    }
    new_order = create_order(order)

    return new_order


create_payment_result = UnionType("CreatePaymentResult")


@create_payment_result.type_resolver
def resolve_create_payment_result(obj, *_):
    if ("success" in obj):
        return "SuccessPaymentCreation"
    return "ErrorUnknown"


@mutation.field("createPayment")
def resolve_create_payment(obj, info, input):
    return {
        "success": true
    }

    

get_user_result = UnionType("GetUserResult")

@get_user_result.type_resolver
def resolve_get_user_result_type(obj, *_):
    if ("user" in obj):
        return "SuccessfullyGetUser"
    return "ErrorAuth"

@query.field("getUser")
def resolve_get_user(obj, info, input):
    return {
        "user": {
            "id": 107,
            "name": "John Jackson",
            "email": "john@gmail.com",
            "wallet": {
                "id": 4,
                "user_id": 107,
                "balance": 1090,
            }
        }
    }


@query.field("getOrdersList")
def resolve_get_orders_list(obj, info, input):
    id = input["userId"]
    last_id = input.get("lastId")
    order_status = input.get("orderStatus")

    created_at = datetime.now()
    
    return {
        "orders": [
            {
                "id": 1,
                "idempotency_key": "1a2bc3",
                "user_id": 103,
                "total_price": 20000,
                "created_at": created_at,
                "status": "PENDING",
                "items": [
                    {
                        "id": 1,
                        "product": {
                            "id": 1,
                            "name": "Iphone 17",
                            "price": 10000
                        },
                        "product_price_freezed": 10000,
                        "quantity": 2,
                    },
                ]
            },
        ]
    }


@query.field("getProductList")
def resolve_get_products_list(obj, info, input):
    return {
        "products": [{
            "id": 1,
            "name": "Iphone 17",
            "price": 10000
        },
        {
            "id": 2,
            "name": "Moby Dick Book",
            "price": 204
        },
        {
            "id": 3,
            "name": "Flowers",
            "price": 170
        },]
    }

schema = make_executable_schema(type_defs, query, mutation, snake_case_fallback_resolvers, get_user_result)
app = GraphQL(schema, debug=True)