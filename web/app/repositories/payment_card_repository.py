from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.payment_card import PaymentCard
from app.repositories.base_repository import BaseRepository


class PaymentCardRepository(BaseRepository):
    """
    Payment Card repository.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_by_id(
        self,
        card_id: int,
    ) -> PaymentCard | None:
        result = await self.session.execute(
            select(PaymentCard).where(
                PaymentCard.id == card_id
            )
        )
        return result.scalar_one_or_none()

    async def get_all_cards(
        self,
    ) -> list[PaymentCard]:
        result = await self.session.execute(
            select(PaymentCard).order_by(
                PaymentCard.sort_order,
                PaymentCard.id,
            )
        )
        return list(result.scalars().all())

    async def get_active_cards(
        self,
    ) -> list[PaymentCard]:
        result = await self.session.execute(
            select(PaymentCard)
            .where(
                PaymentCard.is_active.is_(True)
            )
            .order_by(
                PaymentCard.sort_order,
                PaymentCard.id,
            )
        )
        return list(result.scalars().all())

    async def create(
        self,
        card: PaymentCard,
    ) -> PaymentCard:
        self.session.add(card)
        await self.session.flush()
        await self.session.refresh(card)
        return card

    async def update(
        self,
        card: PaymentCard,
    ) -> PaymentCard:
        await self.session.flush()
        await self.session.refresh(card)
        return card

    async def delete(
        self,
        card: PaymentCard,
    ) -> None:
        await self.session.delete(card)
        await self.session.flush()
