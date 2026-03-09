# Этот файл не является тестом — используется для быстрого заполнения БД через shell.
# Запуск: python manage.py seed_db
# Или напрямую: python manage.py shell < core/infrastructure/tests/test_factories.py

from core.infrastructure.tests.factories import (
    IdempotencyRecordsFactory,
    OrderFactory,
    OrderProductsFactory,
    ProductFactory,
    RefundFactory,
    UserFactory,
    WalletFactory,
)

products = ProductFactory.create_batch(10)

for _ in range(5):
    user = UserFactory()
    WalletFactory(user=user)

    order = OrderFactory(user=user, status="PAID")
    for product in products[:3]:
        OrderProductsFactory(order=order, product=product)
    RefundFactory(order=order)

    order_pending = OrderFactory(user=user, status="PENDING")
    for product in products[3:6]:
        OrderProductsFactory(order=order_pending, product=product)

IdempotencyRecordsFactory.create_batch(10)

print("Данные успешно добавлены в БД")
