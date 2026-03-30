from abc import ABC, abstractmethod
from typing import Optional, List

from core.domain.entities import ProductEntity, UserEntity, OrderEntity, PaymentEntity
from core.domain.value_objects import OrderProduct


class IProductRepository(ABC):
    @abstractmethod
    def get_product_by_id(self, product_id: int) -> Optional[ProductEntity]:
        pass

    @abstractmethod
    def get_all(self, last_id: int, limit: int) -> List[ProductEntity]:
        pass



# todo: избавиться от optional
class IUserRepository(ABC):
    @abstractmethod
    def get_user(self, user_id: int) -> Optional[UserEntity]:
        pass


class IOrderRepository(ABC):
    @abstractmethod
    def get_order(self, order_id) -> Optional[OrderEntity]:
        pass

    @abstractmethod
    def get_all(self, user_id: int, order_status, last_id: int, limit: int) -> List[OrderEntity]:
        pass

    @abstractmethod
    def create_order(self, user_id: int, idempotency_key: str, items: List[OrderProduct]):
        pass


class IPaymentRepository(ABC):
    @abstractmethod
    def create_payment(self, idempotency_key: str, order_id: int, wallet_id: int): 
        pass

