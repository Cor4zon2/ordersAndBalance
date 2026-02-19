from django.test import TestCase
from core.models import BalanceLedger

class BalanceModelTests(TestCase):
    def test_happy_path(self):
        b = BalanceLedger.objects.create(balance=100)
        self.assertEqual(str(b), "100")