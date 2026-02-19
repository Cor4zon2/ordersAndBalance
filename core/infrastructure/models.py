from django.db import models

class Order(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    created_at = models.DateField()

    def __str__(self):
        return self.title


class BalanceLedger(models.Model):
    balance = models.FloatField(default=0)

    def __str__(self):
        return str(self.balance)


class Payment(models.Model):
    amount = models.FloatField(default=0)
    created_at = models.DateField()
    balance_ledger = models.ForeignKey(
        BalanceLedger,
        on_delete=models.CASCADE,
    )
    
    def __str__(self):
        return str(self.amount)


class Refund(models.Model):
    created_at = models.DateField()

    def __str__(self):
        return self.createdAt


