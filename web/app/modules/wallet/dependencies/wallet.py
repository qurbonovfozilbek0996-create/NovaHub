from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies.services import get_db_session
from app.modules.wallet.repositories.wallet_repository import (
    WalletRepository,
)
from app.modules.wallet.services.wallet_service import WalletService


def get_wallet_repository(
    session: AsyncSession = Depends(get_db_session),
) -> WalletRepository:
    """
    Wallet Repository dependency.
    """

    return WalletRepository(session)


def get_wallet_service(
    session: AsyncSession = Depends(get_db_session),
    repository: WalletRepository = Depends(get_wallet_repository),
) -> WalletService:
    """
    Wallet Service dependency.
    """

    return WalletService(
        session=session,
        repository=repository,
    )
