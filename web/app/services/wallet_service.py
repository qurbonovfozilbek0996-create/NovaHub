from sqlalchemy.ext.asyncio import AsyncSession

from app.core.uow.unit_of_work import UnitOfWork

from app.models.transaction import Transaction
from app.models.wallet import Wallet

from app.repositories.transaction_repository import (
    TransactionRepository,
)
from app.repositories.wallet_repository import WalletRepository

from app.services.base_service import BaseService

from app.utils.wallet_id import WalletIdGenerator

class WalletService(BaseService):
    """
    NovaHub Wallet Service.

    Wallet bilan bog'liq barcha biznes qoidalarining
    yagona kirish nuqtasi.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(session)

        self.wallets = WalletRepository(session)
        self.transactions = TransactionRepository(session)
        self.uow = UnitOfWork(session)

    async def create_wallet(
        self,
        user_id: int,
    ) -> Wallet:
        """
        Create wallet for user if it does not exist.
        """

        existing_wallet = await self.wallets.get_by_user_id(
            user_id
        )

        if existing_wallet is not None:
            return existing_wallet

        last_wallet = await self.wallets.get_last_wallet()

        wallet = Wallet(
            user_id=user_id,
            wallet_id=WalletIdGenerator.next_from_wallet(
                last_wallet
            ),
            balance=0,
            is_active=True,
            is_locked=False,
        )

        async with self.uow:
            return await self.wallets.create(wallet)

    async def get_wallet(
        self,
        user_id: int,
    ) -> Wallet | None:
        """
        Foydalanuvchining walletini qaytaradi.
        """
        return await self.wallets.get_by_user_id(user_id)

    async def get_wallet_by_wallet_id(
        self,
        wallet_id: str,
    ) -> Wallet | None:
        """
        Wallet ID (masalan: WL000001) orqali walletni qaytaradi.
        """
        return await self.wallets.get_by_wallet_id(wallet_id)

    async def get_wallet_by_id(
        self,
        wallet_id: int,
    ) -> Wallet | None:
        """
        Wallet database ID orqali topish.
        """
        return await self.wallets.get_by_id(
            wallet_id
        )

    async def wallet_exists(
        self,
        user_id: int,
    ) -> bool:
        """
        Foydalanuvchida wallet mavjudligini tekshiradi.
        """
        wallet = await self.get_wallet(user_id)
        return wallet is not None

    async def add_balance(
        self,
        wallet: Wallet,
        amount: int,
        transaction_type: str = "deposit",
        description: str | None = None,
    ) -> Wallet:
        """
        Wallet balansiga mablag' qo'shadi
        va transaction yaratadi.
        """

        if amount <= 0:
            raise ValueError(
                "Mablag' 0 dan katta bo'lishi kerak."
            )

        if not wallet.is_active:
            raise ValueError(
                "Wallet faol emas."
            )

        if wallet.is_locked:
            raise ValueError(
                "Wallet bloklangan."
            )

        balance_before = wallet.balance

        wallet.balance += amount

        transaction = Transaction(
            transaction_id=f"TXN-{wallet.id}-{balance_before}",
            wallet_id=wallet.id,
            type=transaction_type,
            status="completed",
            amount=amount,
            commission=0,
            cashback=0,
            balance_before=balance_before,
            balance_after=wallet.balance,
            description=description,
        )

        async with self.uow:
            self.session.add(transaction)

            await self.session.flush()
            await self.session.refresh(wallet)

        return wallet
