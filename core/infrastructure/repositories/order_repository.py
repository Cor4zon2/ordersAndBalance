from core.domain.interfaces import IOrderRepository
from core.infrastructure.models import Order, Status
from core.domain.entities import OrderProductEntity, OrderEntity, ProductEntity

from typing import Optional, List

class DjangoOrderRepository(IOrderRepository):
    def get_order(self, order_id) -> Optional[OrderEntity]:
        order = Order.objects.filter(id = order_id).first()
        return OrderEntity(
            id=order.id,
            user_id=order.user.id,
            total_price=order.total_price,
            status=Status(order.status).name,
            # это ошибка. Но запрос не используется в схеме. Пока пропущу
            items=[]
        )
        


    def get_all(self, user_id, order_status, last_id, limit) -> List[OrderEntity]:
        orders = Order.objects.prefetch_related("items__product").filter(user_id=user_id, id__gt=last_id)

        if order_status:
            orders = orders.filter(status=Status[order_status])

        orders = orders.order_by("id")[:limit]
        
        result = []

        for order in orders:
            order_items = []

            for item in order.items.all():
                entity = OrderProductEntity(
                    id=item.id,
                    product=ProductEntity(
                        id=item.product.id,
                        name=item.product.name,
                        price=item.product.price,
                    ),
                    product_price_freezed=item.product_price_freezed,
                    quantity=item.quantity,
                )

                order_items.append(entity)
            
            result.append(OrderEntity(
                id=order.id,
                user_id=order.user.id,
                idempotency_key=order.idempotency_key,
                total_price=order.total_price,
                created_at=order.created_at,
                status=Status(order.status).name,
                items=order_items,
            ))

        return result




