from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.payment import Payment
from app.repositories.base_repository import BaseRepository


class PaymentRepository(BaseRepository):
    """
    Payment repository.
    """

    def __init__(
        self,
        session: AsyncSession,
    ):
        super().__init__(session)

    async def get_by_id(
        self,
        payment_id: int,
    ) -> Payment | None:
        result = await self.session.execute(
            select(Payment).where(
                Payment.id == payment_id
            )
        )

        return result.scalar_one_or_none()

    async def get_pending(
        self,
    ) -> list[Payment]:
        result = await self.session.execute(
            select(Payment)
            .where(
                Payment.status == "pending"
            )
            .order_by(
                Payment.created_at.desc()
            )
        )

        return list(result.scalars().all())

    async def create(
        self,
        payment: Payment,
    ) -> Payment:
        self.session.add(payment)

        await self.session.flush()
        await self.session.refresh(payment)

        return payment

    async def update(
        self,
        payment: Payment,
    ) -> Payment:
        await self.session.flush()
        await self.session.refresh(payment)

        return payment
