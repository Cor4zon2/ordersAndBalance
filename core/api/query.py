from ariadne import gql, QueryType, make_executable_schema, MutationType, snake_case_fallback_resolvers, UnionType
from ariadne.asgi import GraphQL

from core.infrastructure.models import Order, Refund
from core.infrastructure.repositories.product_repository import DjangoProductRepository 
from core.infrastructure.repositories.user_repository import DjangoUserRepository
from core.infrastructure.repositories.order_repository import DjangoOrderRepository
from core.infrastructure.repositories.payment_repository import DjangoPaymentRepository
from core.domain.domain import create_order, get_products_list, get_user, create_payment, get_orders_list

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
        limit: Int
        orderStatus: OrderStatus
    }

    type GetOrdersListResult {
        orders: [Order!]!
        lastId: ID
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
    idempotency_key = input["idempotencyKey"]
    order_id = input["orderId"]
    wallet_id = input["walletId"]

    payment_repo = DjangoPaymentRepository()
    result = create_payment(payment_repo, idempotency_key, order_id, wallet_id)

    if result == "ERROR_NOT_FOUND":
        return {
        "title": "order or wallet not found",
        "message": "order or wallet not found"
        }

    if result == "ERROR_INSUFFICIENT_FUNDS":
        return {
        "title": "Insufficient balance",
        "message": "Insufficient balance"
        }

    return {
        "success": True
    }
    

get_user_result = UnionType("GetUserResult")

@get_user_result.type_resolver
def resolve_get_user_result_type(obj, *_):
    if ("user" in obj):
        return "SuccessfullyGetUser"
    return "ErrorAuth"

@query.field("getUser")
def resolve_get_user(obj, info, input):
    user_id = input["userId"]
    user_repo = DjangoUserRepository()

    user = get_user(user_repo, user_id)

    return {"user": user}


@query.field("getOrdersList")
def resolve_get_orders_list(obj, info, input):
    user_id = input["userId"]
    last_id = input.get("lastId", 0)
    limit = input.get("limit", 10)
    order_status = input.get("orderStatus")

    orders_repo = DjangoOrderRepository()
    
    orders = get_orders_list(orders_repo, user_id, last_id, limit, order_status)
    return {
        "orders": orders,
        "last_id": orders[-1]["id"] if orders else None
        }    



@query.field("getProductList")
def resolve_get_products_list(obj, info, input):
    lastId = input["lastId"]
    product_repo = DjangoProductRepository()
    products = get_products_list(product_repo, lastId)
    return { "products": products }

schema = make_executable_schema(type_defs, query, mutation, snake_case_fallback_resolvers, get_user_result, create_payment_result)
app = GraphQL(schema, debug=True)