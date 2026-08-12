from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth.auth_context import AuthContext
from app.core.dependencies.current_user import get_current_user
from app.core.dependencies.services import get_db_session
from app.modules.payments.dependencies.payment import (
    get_payment_service,
)
from app.modules.payments.services.payment_service import PaymentService
from app.modules.wallet.dependencies.wallet import get_wallet_service
from app.modules.wallet.services.wallet_service import WalletService
from app.schemas.payment import PaymentCreate


router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)


@router.post("/")
async def create_payment(
    data: PaymentCreate,
    auth: AuthContext = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
    service: PaymentService = Depends(get_payment_service),
    wallet_service: WalletService = Depends(get_wallet_service),
):
    """
    User payment request yaratadi.

    Current user Telegram WebApp autentifikatsiyasi orqali
    aniqlanadi va payment uning walletiga biriktiriladi.
    """

    wallet = await wallet_service.get_by_user_id(
        auth.user.id
    )

    if wallet is None:
        raise HTTPException(
            status_code=404,
            detail="Foydalanuvchi walleti topilmadi.",
        )

    try:
        payment = await service.create_payment(
            wallet_id=wallet.id,
            payment_card_id=data.payment_card_id,
            amount=data.amount,
            receipt_image=data.receipt_image,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    return {
        "success": True,
        "item": payment,
    }
