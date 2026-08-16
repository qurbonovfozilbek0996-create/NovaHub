from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.orders.models.order import Order
from app.modules.services.models.service import Service


class OrderService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_order(
        self,
        user_id: int,
        service_id: int,
        link: str,
        quantity: int,
    ) -> Order:
        service = await self.session.get(Service, service_id)

        if service is None:
            raise ValueError("Xizmat topilmadi.")

        if not service.is_active:
            raise ValueError("Bu xizmat hozir faol emas.")

        link = link.strip()

        if not link:
            raise ValueError("Havola kiritilmagan.")

        if quantity < service.min_quantity:
            raise ValueError(
                f"Miqdor minimal {service.min_quantity} bo‘lishi kerak."
            )

        if quantity > service.max_quantity:
            raise ValueError(
                f"Miqdor maksimal {service.max_quantity} bo‘lishi kerak."
            )

        unit_price = Decimal(str(service.sale_price or 0))
        total_price = unit_price * Decimal(quantity)

        order = Order(
            user_id=user_id,
            service_id=service.id,
            provider_id=service.provider_id,
            link=link,
            quantity=quantity,
            unit_price=unit_price,
            total_price=total_price,
            status="pending",
        )

        self.session.add(order)

        await self.session.commit()
        await self.session.refresh(order)

        return order
