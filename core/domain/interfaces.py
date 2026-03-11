from abc import ABC, abstractmethod
from typing import Optional, List

from core.domain.entities import ProductEntity, UserEntity


class IProductRepository(ABC):
    @abstractmethod
    def get_product_by_id(self, product_id: int) -> Optional[ProductEntity]:
        pass

    @abstractmethod
    def get_all(self) -> List[ProductEntity]:
        pass



class IUserRepository(ABC):
    @abstractmethod
    def get_user(self, user_id: int) -> Optional[UserEntity]:
        pass
