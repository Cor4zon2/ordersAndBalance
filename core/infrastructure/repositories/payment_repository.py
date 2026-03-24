from core.infrastructure.models import Payment, Order, Wallet
from core.domain.interfaces import IPaymentRepository
from core.domain.exceptions import InsufficientFundsError, OrderNotFoundError

import structlog
from django.db import transaction

logger = structlog.get_logger()

class DjangoPaymentRepository(IPaymentRepository):
    def create_payment(self, idempotency_key: str, order_id: int, wallet_id: int): 
        # todo: check if there is enoght money for it?
        with transaction.atomic():
            order_price = Order.objects.filter(id=order_id).values_list("total_price", flat=True).first()
            balance = Wallet.objects.filter(id=wallet_id).values_list("balance", flat=True).first()

            if order_price is None or balance is None:
                logger.error("create_payment", order_id=order_id, wallet_id=wallet_id)
                raise OrderNotFoundError()

            if (order_price > balance):
                logger.error("create_payment", order_id=order_id, wallet_id=wallet_id)
                raise InsufficientFundsError()

            return Payment.objects.create(idempotency_key=idempotency_key, order_id=order_id, wallet_id=wallet_id, price=order_price)