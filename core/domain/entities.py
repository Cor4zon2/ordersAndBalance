from dataclasses import dataclass
from typing import List
from enum import Enum


def create_order(order):
    return {
        "id": "mock-id",
        "items": [
            {"id": 1, "name": "Iphone 17", "amount": 3},
            {"id": 2, "name": "New TV", "amount": 1},
            {"id": 3, "name": "Book", "amount": 2}
            ],
        "price": 1000,
        "clientId": 101,
        "status": "PAID"
    }


def get_order_by_id(id):
    return {
        "id": "mock-id",
        "items": [
            {"id": 21, "name": "Socks", "amount": 1},
            {"id": 32, "name": "MusicBox", "amount": 1},
            {"id": 13, "name": "Book", "amount": 22}
            ],
        "price": 55,
        "clientId": 10,
        "status": "PENDING"
    }


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
class OrderProduct:
    id: int
    product: ProductEntity
    price_freezed: int
    quantity: int

class OrderStatus(Enum):
    PENDING = 'PENDING'
    PAID = 'PAID'
    CANCELED = 'CANCELED'
    

@dataclass
class OrderEntity:
    id: int
    user_id: int
    total_price: int
    created_at: str
    status: OrderStatus
    items: List[OrderProduct]


@dataclass
class PaymentEntity:
    id: int