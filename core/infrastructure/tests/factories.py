import uuid

import factory
from factory import Faker, LazyFunction, SubFactory
from factory.django import DjangoModelFactory

from core.infrastructure.models import (
    IdempotencyRecords,
    Order,
    OrderProducts,
    Product,
    Refund,
    User,
    Wallet,
)


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    name = Faker("name", locale="ru_RU")
    email = Faker("email")


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = Faker("word")
    price = Faker("random_int", min=100, max=100_000)


class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order

    idempotency_key = LazyFunction(uuid.uuid4)
    user = SubFactory(UserFactory)
    total_price = Faker("random_int", min=0, max=1_000_000)
    status = factory.Iterator(["PENDING", "PAID", "CANCELED"])


class OrderProductsFactory(DjangoModelFactory):
    class Meta:
        model = OrderProducts

    order = SubFactory(OrderFactory)
    product = SubFactory(ProductFactory)
    quantity = Faker("random_int", min=1, max=10)
    product_price_freezed = Faker("random_int", min=100, max=100_000)


class WalletFactory(DjangoModelFactory):
    class Meta:
        model = Wallet

    user = SubFactory(UserFactory)
    balance = Faker("random_int", min=0, max=1_000_000)


class IdempotencyRecordsFactory(DjangoModelFactory):
    class Meta:
        model = IdempotencyRecords

    idempotency_key = LazyFunction(uuid.uuid4)
    namespace = Faker("word")
    status = factory.Iterator(["PENDING", "SUCCESS", "FAILED"])


class RefundFactory(DjangoModelFactory):
    class Meta:
        model = Refund

    idempotency_key = LazyFunction(uuid.uuid4)
    order = SubFactory(OrderFactory)
    reason = Faker("sentence")
