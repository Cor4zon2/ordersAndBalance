from django.db import models

class Order(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    created_at = models.DateField()

    def __str__(self):
        return str(self.title)


class BalanceLedger(models.Model):
    balance = models.FloatField(default=0)

    def __str__(self):
        return str(self.balance)


class Payment(models.Model):
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateField()
    balance_ledger = models.OneToOneField(
        BalanceLedger,
        on_delete=models.CASCADE,
    )
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    
    def __str__(self):
        return str(self.amount)


class Refund(models.Model):
    created_at = models.DateField()
    reason = models.CharField(max_length=1000, default="-")
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return str(self.reason)


