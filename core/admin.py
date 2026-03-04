from django.contrib import admin

from .models import Order, BalanceLedger, Refund

admin.site.register(Order)
admin.site.register(BalanceLedger)
admin.site.register(Refund)