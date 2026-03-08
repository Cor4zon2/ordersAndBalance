from django.contrib import admin

from .models import Order, Refund, OrderProducts, Product, User, Wallet, IdempotencyRecords

admin.site.register(Order)
admin.site.register(Refund)
admin.site.register(OrderProducts)
admin.site.register(Product)
admin.site.register(User)
admin.site.register(Wallet)
admin.site.register(IdempotencyRecords)