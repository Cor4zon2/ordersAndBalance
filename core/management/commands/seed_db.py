from django.core.management.base import BaseCommand

from core.infrastructure.tests.factories import (
    IdempotencyRecordsFactory,
    OrderFactory,
    OrderProductsFactory,
    PaymentFactory,
    ProductFactory,
    RefundFactory,
    UserFactory,
    WalletFactory,
)


class Command(BaseCommand):
    help = "Заполнить БД тестовыми данными через фабрики"

    def add_arguments(self, parser):
        parser.add_argument(
            "--users", type=int, default=5, help="Количество пользователей (по умолчанию 5)"
        )
        parser.add_argument(
            "--products", type=int, default=10, help="Количество продуктов (по умолчанию 10)"
        )

    def handle(self, *args, **options):
        n_users = options["users"]
        n_products = options["products"]

        self.stdout.write("Создаём продукты...")
        products = ProductFactory.create_batch(n_products)

        self.stdout.write(f"Создаём {n_users} пользователей с кошельками и заказами...")
        for i in range(n_users):
            user = UserFactory()
            wallet = WalletFactory(user=user)

            # Заказ PENDING
            order_pending = OrderFactory(user=user, status="PENDING")
            for product in products[:3]:
                OrderProductsFactory(order=order_pending, product=product)

            # Заказ PAID с возвратом
            order_paid = OrderFactory(user=user, status="PAID")
            for product in products[3:6]:
                OrderProductsFactory(order=order_paid, product=product)
            PaymentFactory(wallet=wallet, order=order_paid, status="PAID", price=order_paid.total_price)
            RefundFactory(order=order_paid)

            # Заказ CANCELED
            order_canceled = OrderFactory(user=user, status="CANCELED")
            for product in products[6:8]:
                OrderProductsFactory(order=order_canceled, product=product)

        self.stdout.write("Создаём записи идемпотентности...")
        IdempotencyRecordsFactory.create_batch(10)

        self.stdout.write(self.style.SUCCESS(
            f"\nГотово! Создано:\n"
            f"  Пользователей:       {n_users}\n"
            f"  Кошельков:           {n_users}\n"
            f"  Продуктов:           {n_products}\n"
            f"  Заказов:             {n_users * 3}\n"
            f"  Позиций в заказах:   {n_users * 8}\n"
            f"  Платежей:            {n_users}\n"
            f"  Возвратов:           {n_users}\n"
            f"  Записей идемпот.:    10\n"
        ))
