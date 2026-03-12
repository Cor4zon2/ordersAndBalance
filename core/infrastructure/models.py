from django.db import models
import uuid


class Status(models.TextChoices):
        PENDING = 'PENDING', 'Ожидает оплаты'
        PAID = 'PAID', 'Оплачен'
        CANCELED = 'CANCELED', 'Отменен'

class User(models.Model):
    name = models.CharField("Имя пользователя", max_length=200)
    email = models.EmailField("Email пользователя", max_length=200)

    def __str__(self):
        return f"{self.name}"


class Order(models.Model):
    idempotency_key = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    total_price = models.IntegerField(default=0, verbose_name="Цена")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING, verbose_name="Статус")

    def __str__(self):
        return f"Заказ {self.id} от {self.user}"


class Product(models.Model):
    name = models.CharField(max_length=300)
    price = models.IntegerField()

    def __str__(self):
        return f"{self.name}"


class OrderProducts(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE, default=1, verbose_name="Продукт")
    order = models.ForeignKey(
        Order, 
        on_delete = models.CASCADE, 
        related_name="items",
        default=1,
        verbose_name="Заказ",
        )
    quantity = models.IntegerField("Количество", default=1)
    product_price_freezed = models.IntegerField("Фиксированная цена заказа", default=1)
    
    def __str__(self):
        return f"Цена {self.id}: {self.product_price_freezed}"


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    balance = models.IntegerField("Баланс кошелька")

    def __str__(self):
        return f"Пользователь {self.user} имеет {self.balance} на счету"

class IdempotencyRecords(models.Model):
    idempotency_key = models.CharField("Ключ идемпотентности", max_length=200, unique=True, default=uuid.uuid4)
    namespace = models.CharField(max_length=200)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True )



class Refund(models.Model):
    idempotency_key = models.CharField("Ключ идемпотентности", max_length=200, unique=True, default=uuid.uuid4)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    reason = models.CharField(max_length=200)
    created_at =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заказ {self.order} был вовращен {self.created_at} по причине: {self.reason}"


class Payment(models.Model):
    idempotency_key = models.CharField("Ключ идемпотентности", max_length=200, unique=True, default=uuid.uuid4)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, verbose_name="Кошелек пользователя")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Заказ")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING, verbose_name="Статус платежа")
    price = models.IntegerField("Сумма платежа")

    def __str__(self):
        return f"Оплата заказа {self.order} от {self.created_at} со статусом {self.status}"


