from typing import Optional, Dict

from core.domain.interfaces import IProductRepository
from core.infrastructure.models import Product


class DjangoProductRepository(IProductRepository):
    def get_product_by_id(self, product_id: int) -> Optional[dict]:
        return Product.objects.filter(id = product_id).values("id", "name", "price").first()


    def get_all(self) -> Dict[int, dict]:
        products = Product.objects.values("id", "name", "price")
        return {item["id"] : {
            "name": item["name"],
            "price": item["price"]
        } for item in products}