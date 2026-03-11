from dataclasses import dataclass
from typing import List

from django.db import transaction

from core.domain.interfaces import IProductRepository



def get_user(user_id: int):
    pass


def get_orders_list(user_id: int, last_id: int, order_status):
    pass


def get_products_list(prodcut_repo: IProductRepository,last_id: int):
    products_dict = prodcut_repo.get_all()
    return [{"id": p_id, "name": p_info["name"], "price": p_info["price"]} for p_id, p_info in products_dict.items()]
    


def get_payments_list(user_id: int, last_id: int):
    pass


def parse_items(items):
    return {}

@dataclass
class OrderProductDTO:
    productId: int
    quantity: int



def create_order(user_id: int, idempotency_key: str, products: List[OrderProductDTO]):
    with transaction.atomic:
        already_processed = itempotency_repository.check_key(idempotency_key)

        if already_processed:
            # возващаем success или ошибку, уже был создан
            pass


        product_ids = [item.productId for item in products]

        order_id = order_repository.create_order(user_id, idempotency_key, items)
        orderProducts_repository.create_order_products(products, order_id)
        itempotency_repository.save_key(idempotency_key)
    
        return {}

def create_refund(order_id: int, user_id: int, reason: str, idempotency_key: str):
    pass


def create_payment(idempotency_key: str, order_id: int, wallet_id: int):
    pass