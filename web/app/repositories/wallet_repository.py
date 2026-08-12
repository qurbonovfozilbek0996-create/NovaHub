from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.wallet import Wallet
from app.repositories.base_repository import BaseRepository


class WalletRepository(BaseRepository):
    """
    Wallet repository.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_by_id(self, wallet_id: int) -> Wallet | None:
        result = await self.session.execute(
            select(Wallet).where(Wallet.id == wallet_id)
        )
        return result.scalar_one_or_none()

    async def get_by_wallet_id(
        self,
        wallet_code: str,
    ) -> Wallet | None:
        result = await self.session.execute(
            select(Wallet).where(
                Wallet.wallet_id == wallet_code
            )
        )
        return result.scalar_one_or_none()

    async def get_by_user_id(
        self,
        user_id: int,
    ) -> Wallet | None:
        result = await self.session.execute(
            select(Wallet).where(
                Wallet.user_id == user_id
            )
        )
        return result.scalar_one_or_none()

    async def get_last_wallet(self) -> Wallet | None:
        result = await self.session.execute(
            select(Wallet).order_by(Wallet.id.desc()).limit(1)
        )
        return result.scalar_one_or_none()

    async def create(self, wallet: Wallet) -> Wallet:
        self.session.add(wallet)
        await self.session.flush()
        await self.session.refresh(wallet)
        return wallet
