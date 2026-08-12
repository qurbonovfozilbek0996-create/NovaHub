from fastapi import APIRouter, Depends, HTTPException

from app.modules.payments.dependencies.payment import (
    get_payment_service,
)
from app.modules.payments.services.payment_service import PaymentService


router = APIRouter(
    prefix="/admin/payments",
    tags=["Admin Payments"],
)


@router.get("/")
async def payments_list(
    service: PaymentService = Depends(get_payment_service),
):
    """
    Kutilayotgan paymentlar ro'yxati.
    """

    payments = await service.get_pending_payments()

    return {
        "success": True,
        "count": len(payments),
        "items": payments,
    }


@router.post("/{payment_id}/approve")
async def approve_payment(
    payment_id: int,
    service: PaymentService = Depends(get_payment_service),
):
    """
    Paymentni tasdiqlaydi va wallet balansini oshiradi.
    """

    payment = await service.get_payment_by_id(
        payment_id
    )

    if payment is None:
        raise HTTPException(
            status_code=404,
            detail="Payment topilmadi.",
        )

    try:
        updated = await service.approve_payment(
            payment
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    return {
        "success": True,
        "item": updated,
    }


@router.post("/{payment_id}/reject")
async def reject_payment(
    payment_id: int,
    service: PaymentService = Depends(get_payment_service),
):
    """
    Paymentni rad etadi.
    """

    payment = await service.get_payment_by_id(
        payment_id
    )

    if payment is None:
        raise HTTPException(
            status_code=404,
            detail="Payment topilmadi.",
        )

    try:
        updated = await service.update_status(
            payment,
            "rejected",
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    return {
        "success": True,
        "item": updated,
    }
