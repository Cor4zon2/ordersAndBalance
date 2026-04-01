from core.domain.interfaces import IOrderRepository
from core.infrastructure.models import Order, Status, IdempotencyRecords, OrderProducts, Product
from core.domain.entities import OrderProductEntity, OrderEntity, ProductEntity
from core.domain.value_objects import OrderProduct
from django.db import transaction

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


    def create_order(self, user_id: int, idempotency_key: str, items: List[OrderProduct]):
        
        with transaction.atomic():            
            exists = IdempotencyRecords.objects.select_for_update().filter(idempotency_key=idempotency_key).exists()
            if exists:
                return
            IdempotencyRecords.objects.create(idempotency_key=idempotency_key, namespace="order")
                
            
            total_price = 0

            new_order = Order.objects.create(user_id=user_id, idempotency_key=idempotency_key, total_price=total_price)

            for item in items:
                order_id = new_order.id
                product_price = Product.objects.filter(id=item["productId"]).values_list("price", flat=True).first()
                total_price = total_price + product_price

                OrderProducts.objects.create(
                    product_id=item["productId"],
                    order_id=order_id,
                    quantity=item["quantity"],
                    product_price_freezed=product_price,
                )

            new_order.total_price = total_price
            new_order.save(update_fields=["total_price"])

            

        