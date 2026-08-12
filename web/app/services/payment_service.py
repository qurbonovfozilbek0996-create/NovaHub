from sqlalchemy.ext.asyncio import AsyncSession

from app.core.uow.unit_of_work import UnitOfWork

from app.models.payment import Payment
from app.repositories.payment_repository import PaymentRepository

from app.services.base_service import BaseService
from app.models.wallet import Wallet
from app.services.wallet_service import WalletService


class PaymentService(BaseService):
    """
    NovaHub Payment Service.

    Wallet to'ldirish to'lovlari
    biznes qoidalarining yagona kirish nuqtasi.
    """

    def __init__(
        self,
        session: AsyncSession,
    ):
        super().__init__(session)

        self.payments = PaymentRepository(session)
        self.uow = UnitOfWork(session)
        self.wallets = WalletService(session)

    async def get_payment_by_id(
        self,
        payment_id: int,
    ) -> Payment | None:
        return await self.payments.get_by_id(
            payment_id
        )

    async def get_pending_payments(
        self,
    ) -> list[Payment]:
        return await self.payments.get_pending()

    async def create_payment(
        self,
        *,
        wallet_id: int,
        payment_card_id: int | None,
        amount: int,
        receipt_image: str | None = None,
    ) -> Payment:

        payment = Payment(
            wallet_id=wallet_id,
            payment_card_id=payment_card_id,
            amount=amount,
            status="pending",
            receipt_image=receipt_image,
        )

        async with self.uow:
            return await self.payments.create(
                payment
            )

    async def update_status(
        self,
        payment: Payment,
        status: str,
        admin_note: str | None = None,
    ) -> Payment:

        payment.status = status

        if admin_note:
            payment.admin_note = admin_note

        async with self.uow:
            return await self.payments.update(
                payment
            )

    async def approve_payment(
        self,
        payment: Payment,
        admin_note: str | None = None,
    ) -> Payment:
        """
        Payment tasdiqlash.
        Wallet balansini oshiradi.
        """

        if payment.status != "pending":
            raise ValueError(
                "Bu payment allaqachon ko'rib chiqilgan."
            )

        wallet = await self.wallets.get_wallet_by_id(
            payment.wallet_id
        )

        if wallet is None:
            raise ValueError(
                "Wallet topilmadi."
            )

        await self.wallets.add_balance(
            wallet=wallet,
            amount=payment.amount,
            transaction_type="deposit",
            description=f"Payment #{payment.id} approved",
        )

        payment.status = "approved"

        if admin_note:
            payment.admin_note = admin_note

        async with self.uow:
            return await self.payments.update(
                payment
            )
