from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions.not_found import NotFoundException
from app.core.uow.unit_of_work import UnitOfWork

from app.models.payment_card import PaymentCard

from app.repositories.payment_card_repository import (
    PaymentCardRepository,
)

from app.services.base_service import BaseService


class PaymentCardService(BaseService):
    """
    NovaHub Payment Card Service.

    To'lov kartalari bilan bog'liq barcha
    biznes qoidalarining yagona kirish nuqtasi.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(session)

        self.cards = PaymentCardRepository(session)
        self.uow = UnitOfWork(session)

    async def get_card_by_id(
        self,
        card_id: int,
    ) -> PaymentCard:
        card = await self.cards.get_by_id(card_id)

        if not card:
            raise NotFoundException(
                "Payment card not found."
            )

        return card

    async def get_all_cards(
        self,
    ) -> list[PaymentCard]:
        return await self.cards.get_all_cards()

    async def get_active_cards(
        self,
    ) -> list[PaymentCard]:
        return await self.cards.get_active_cards()

    async def create_card(
        self,
        *,
        card_name: str,
        card_number: str,
        card_holder: str,
        min_amount: int,
        max_amount: int,
        payment_note: str | None = None,
        qr_image: str | None = None,
        sort_order: int = 1,
        is_active: bool = True,
    ) -> PaymentCard:
        card = PaymentCard(
            card_name=card_name,
            card_number=card_number,
            card_holder=card_holder,
            min_amount=min_amount,
            max_amount=max_amount,
            payment_note=payment_note,
            qr_image=qr_image,
            sort_order=sort_order,
            is_active=is_active,
        )

        async with self.uow:
            return await self.cards.create(card)

    async def update_card(
        self,
        card: PaymentCard,
    ) -> PaymentCard:
        async with self.uow:
            return await self.cards.update(card)

    async def delete_card(
        self,
        card: PaymentCard,
    ) -> None:
        async with self.uow:
            await self.cards.delete(card)
