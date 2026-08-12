from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies.services import get_db_session
from app.modules.payments.repositories.payment_repository import (
    PaymentRepository,
)
from app.modules.payments.services.payment_service import PaymentService
from app.modules.wallet.dependencies.wallet import get_wallet_service
from app.modules.wallet.services.wallet_service import WalletService


def get_payment_repository(
    session: AsyncSession = Depends(get_db_session),
) -> PaymentRepository:
    """
    Payment Repository dependency.
    """

    return PaymentRepository(session)


def get_payment_service(
    session: AsyncSession = Depends(get_db_session),
    repository: PaymentRepository = Depends(
        get_payment_repository,
    ),
    wallet_service: WalletService = Depends(
        get_wallet_service,
    ),
) -> PaymentService:
    """
    Payment Service dependency.
    """

    return PaymentService(
        session=session,
        repository=repository,
        wallet_service=wallet_service,
    )
