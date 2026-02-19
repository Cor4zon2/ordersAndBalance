from django.contrib import admin

from .models import Order, BalanceLedger

admin.site.register(Order)
admin.site.register(BalanceLedger)