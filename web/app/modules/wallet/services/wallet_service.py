from sqlalchemy.ext.asyncio import AsyncSession

from app.models.transaction import Transaction
from app.models.wallet import Wallet
from app.modules.wallet.repositories.wallet_repository import (
    WalletRepository,
)
from app.core.uow.unit_of_work import UnitOfWork
from app.utils.wallet_id import WalletIdGenerator


class WalletService:
    """
    NovaHub Wallet biznes logikasi.

    Wallet bilan bog'liq barcha asosiy operatsiyalar
    shu service orqali boshqariladi.
    """

    def __init__(
        self,
        session: AsyncSession,
        repository: WalletRepository,
    ):
        self.session = session
        self.repository = repository
        self.uow = UnitOfWork(session)

    async def get_by_id(
        self,
        wallet_id: int,
    ) -> Wallet | None:
        """
        Database ID orqali walletni topadi.
        """

        return await self.repository.get_by_id(wallet_id)

    async def get_by_user_id(
        self,
        user_id: int,
    ) -> Wallet | None:
        """
        Foydalanuvchining walletini topadi.
        """

        return await self.repository.get_by_user_id(user_id)

    async def get_by_wallet_id(
        self,
        wallet_id: str,
    ) -> Wallet | None:
        """
        Wallet kodi orqali walletni topadi.

        Masalan:
        WL00000001
        """

        return await self.repository.get_by_wallet_id(wallet_id)

    async def wallet_exists(
        self,
        user_id: int,
    ) -> bool:
        """
        Foydalanuvchida wallet mavjudligini tekshiradi.
        """

        wallet = await self.repository.get_by_user_id(user_id)

        return wallet is not None

    async def create_wallet(
        self,
        user_id: int,
    ) -> Wallet:
        """
        Foydalanuvchi uchun wallet yaratadi.

        Agar wallet mavjud bo'lsa,
        mavjud wallet qaytariladi.
        """

        existing_wallet = await self.repository.get_by_user_id(
            user_id
        )

        if existing_wallet is not None:
            return existing_wallet

        last_wallet = await self.repository.get_last_wallet()

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
            return await self.repository.create(wallet)

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
