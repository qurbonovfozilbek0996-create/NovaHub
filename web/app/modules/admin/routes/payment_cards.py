from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies.services import get_db_session

from app.schemas.payment_card import (
    PaymentCardCreate,
    PaymentCardUpdate,
)

from app.services.payment_card_service import PaymentCardService


router = APIRouter(
    prefix="/admin/payment-cards",
    tags=["Admin Payment Cards"],
)


@router.get("/")
async def payment_cards_list(
    session: AsyncSession = Depends(get_db_session),
):
    """
    To'lov kartalari ro'yxati.
    """

    service = PaymentCardService(session)

    cards = await service.get_all_cards()

    return {
        "success": True,
        "count": len(cards),
        "items": cards,
    }


@router.post("/")
async def create_payment_card(
    data: PaymentCardCreate,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Yangi to'lov kartasi yaratish.
    """

    service = PaymentCardService(session)

    card = await service.create_card(
        card_name=data.card_name,
        card_number=data.card_number,
        card_holder=data.card_holder,
        min_amount=data.min_amount,
        max_amount=data.max_amount,
        payment_note=data.payment_note,
        qr_image=data.qr_image,
        sort_order=data.sort_order,
        is_active=data.is_active,
    )

    return {
        "success": True,
        "item": card,
    }


@router.put("/{card_id}")
async def update_payment_card(
    card_id: int,
    data: PaymentCardUpdate,
    session: AsyncSession = Depends(get_db_session),
):
    """
    To'lov kartasini yangilash.
    """

    service = PaymentCardService(session)

    card = await service.get_card_by_id(card_id)

    for key, value in data.model_dump(
        exclude_unset=True
    ).items():
        setattr(card, key, value)

    updated_card = await service.update_card(card)

    return {
        "success": True,
        "item": updated_card,
    }


@router.delete("/{card_id}")
async def delete_payment_card(
    card_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    """
    To'lov kartasini o'chirish.
    """

    service = PaymentCardService(session)

    card = await service.get_card_by_id(card_id)

    await service.delete_card(card)

    return {
        "success": True,
        "message": "Payment card deleted.",
    }
