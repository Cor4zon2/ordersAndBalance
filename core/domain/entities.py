from dataclasses import dataclass
from typing import List
from enum import Enum


class InsufficientFundsError(Exception):
    pass

@dataclass
class UserEntity:
    id: int
    name: str 
    email: str
    wallet_id: int
    wallet_balance: int

    def can_pay(self, amount: int) -> bool:
        if self.wallet_balance < amount:
            raise InsufficientFundsError(f"Недостаточно средств в кошельке: {self.wallet_balance} для оплаты {amount}")

        return True


@dataclass
class ProductEntity:
    id: int
    name: str
    price: int

@dataclass
class OrderProductEntity:
    id: int
    product: ProductEntity
    product_price_freezed: int
    quantity: int

class OrderStatus(Enum):
    PENDING = 'PENDING'
    PAID = 'PAID'
    CANCELED = 'CANCELED'
    

@dataclass
class OrderEntity:
    id: int
    idempotency_key: str
    user_id: int
    total_price: int
    created_at: str
    status: OrderStatus
    items: List[OrderProductEntity]


@dataclass
class PaymentEntity:
    id: int