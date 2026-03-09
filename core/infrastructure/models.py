from django.db import models
import uuid


class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)

    def __str__(self):
        return f"{self.name}"


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Ожидает оплаты'
        PAID = 'PAID', 'Оплачен'
        CANCELED = 'CANCELED', 'Отменен'


    idempotency_key = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=Status.choices ,default=Status.PENDING)

    def __str__(self):
        return f"Заказ {self.id} от {self.user}"


class Product(models.Model):
    name = models.CharField(max_length=300)
    price = models.IntegerField()

    def __str__(self):
        return f"{self.name}"


class OrderProducts(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE, default=1)
    order = models.ForeignKey(Order, on_delete = models.CASCADE, default=1)
    quantity = models.IntegerField(default=1)
    product_price_freezed = models.IntegerField(default=1)
    
    def __str__(self):
        return f"Цена {self.id}: {self.product_price_freezed}"


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.IntegerField()

    def __str__(self):
        return f"Пользователь {self.user} имеет {self.balance} на счету"

class IdempotencyRecords(models.Model):
    idempotency_key = models.CharField(max_length=200, unique=True, default=uuid.uuid4)
    namespace = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True )



class Refund(models.Model):
    idempotency_key = models.CharField(max_length=200, unique=True, default=uuid.uuid4)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    reason = models.CharField(max_length=200)
    created_at =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заказ {self.order} был вовращен {self.created_at} по причине: {self.reason}"





