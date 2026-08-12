from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.transaction import Transaction
from app.repositories.base_repository import BaseRepository


class TransactionRepository(BaseRepository):
    """
    Transaction repository.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_by_id(
        self,
        transaction_id: int,
    ) -> Transaction | None:
        result = await self.session.execute(
            select(Transaction).where(
                Transaction.id == transaction_id
            )
        )
        return result.scalar_one_or_none()

    async def get_by_transaction_id(
        self,
        transaction_code: str,
    ) -> Transaction | None:
        result = await self.session.execute(
            select(Transaction).where(
                Transaction.transaction_id == transaction_code
            )
        )
        return result.scalar_one_or_none()

    async def get_wallet_transactions(
        self,
        wallet_id: int,
    ) -> list[Transaction]:
        result = await self.session.execute(
            select(Transaction)
            .where(Transaction.wallet_id == wallet_id)
            .order_by(Transaction.created_at.desc())
        )
        return list(result.scalars().all())

    async def create(
        self,
        transaction: Transaction,
    ) -> Transaction:
        self.session.add(transaction)
        await self.session.flush()
        await self.session.refresh(transaction)
        return transaction
