from dataclasses import dataclass, asdict
from typing import List

from core.domain.interfaces import IProductRepository, IUserRepository, IOrderRepository, IPaymentRepository
from core.domain.value_objects import OrderProduct



def get_user(user_repo: IUserRepository, user_id: int):
    user_dict = user_repo.get_user(user_id)
    wallet = {
        "id": user_dict.wallet_id,
        "balance": user_dict.wallet_balance,
        "user_id": user_dict.id
    }
    return {"id": user_dict.id, "name": user_dict.name, "email": user_dict.email, "wallet": wallet}


def get_orders_list(orders_repo: IOrderRepository, user_id: int, last_id: int, limit: int, order_status):
    orders_dict = orders_repo.get_all(user_id, order_status, last_id, limit)
    return [asdict(o) for o in orders_dict]
    

def get_products_list(product_repo: IProductRepository, last_id: int, limit: int):
    products_dict = product_repo.get_all(last_id, limit)
    return [{"id": p_id, "name": p_info["name"], "price": p_info["price"]} for p_id, p_info in products_dict.items()]


def get_payments_list(user_id: int, last_id: int):
    pass





def create_order(orders_repo: IOrderRepository, user_id: int, idempotency_key: str, items: List[OrderProduct]):
    new_order = orders_repo.create_order(user_id, idempotency_key, items)
    return new_order





def create_refund(order_id: int, user_id: int, reason: str, idempotency_key: str):
    pass


def create_payment(payment_repo: IPaymentRepository, idempotency_key: str, order_id: int, wallet_id: int):
    return payment_repo.create_payment(idempotency_key=idempotency_key, order_id=order_id, wallet_id=wallet_id)
    