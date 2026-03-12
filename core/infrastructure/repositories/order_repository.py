from core.domain.interfaces import IOrderRepository
from core.infrastructure.models import Order, OrderProducts
from core.domain.entities import OrderEntity

from typing import Optional, List

class DjangoOrderRepository(IOrderRepository):
    def get_order(self, order_id) -> Optional[OrderEntity]:
        return Order.objects.filter(id = order_id).first()
        


    def get_all(self) -> List[OrderEntity]:
        pass
        orders = Order.objects.prefetch_related("items__product").all()
        
        orders_list = []

        for order_object in orders:
            # products_data = 

            entity = OrderEntity(
                id=order_object["id"],
                userId=1,
                total_price=order_object["total_price"],
                created_at=order_object["created_at"],
                status=order_object["status"],
                items=[ ProductEntity(
                    id=item.id, 
                    product={}, 
                    price_freezed=item.price_freezed,
                    quantity=item.quantity
                    )
                     for item in products_data
                ]

            )


        return [{
            "id": item.id,
            "user_id": id,
            "total_price": item["total_price"],
            "status": item["status"],
            "created_at": item["created_at"],
        } for item in orders]