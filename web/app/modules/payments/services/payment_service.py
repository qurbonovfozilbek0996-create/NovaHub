from sqlalchemy.ext.asyncio import AsyncSession

from app.core.uow.unit_of_work import UnitOfWork
from app.models.payment import Payment
from app.modules.payments.repositories.payment_repository import (
    PaymentRepository,
)
from app.modules.wallet.services.wallet_service import WalletService


class PaymentService:
    """
    NovaHub Payment biznes logikasi.

    Wallet to'ldirish paymentlari bilan bog'liq
    barcha asosiy biznes qoidalarining kirish nuqtasi.
    """

    def __init__(
        self,
        session: AsyncSession,
        repository: PaymentRepository,
        wallet_service: WalletService,
    ):
        self.session = session
        self.repository = repository
        self.wallet_service = wallet_service
        self.uow = UnitOfWork(session)

    async def get_payment_by_id(
        self,
        payment_id: int,
    ) -> Payment | None:
        """
        Paymentni database ID orqali topadi.
        """

        return await self.repository.get_by_id(
            payment_id
        )

    async def get_pending_payments(
        self,
    ) -> list[Payment]:
        """
        Kutilayotgan paymentlarni qaytaradi.
        """

        return await self.repository.get_pending()

    async def create_payment(
        self,
        *,
        wallet_id: int,
        payment_card_id: int | None,
        amount: int,
        receipt_image: str | None = None,
    ) -> Payment:
        """
        Yangi payment request yaratadi.
        """

        if wallet_id <= 0:
            raise ValueError(
                "Wallet noto'g'ri."
            )

        if amount <= 0:
            raise ValueError(
                "To'lov miqdori 0 dan katta bo'lishi kerak."
            )

        payment = Payment(
            wallet_id=wallet_id,
            payment_card_id=payment_card_id,
            amount=amount,
            status="pending",
            receipt_image=receipt_image,
        )

        async with self.uow:
            return await self.repository.create(
                payment
            )

    async def update_status(
        self,
        payment: Payment,
        status: str,
        admin_note: str | None = None,
    ) -> Payment:
        """
        Payment statusini yangilaydi.
        """

        allowed_statuses = {
            "pending",
            "approved",
            "rejected",
        }

        if status not in allowed_statuses:
            raise ValueError(
                "Payment statusi noto'g'ri."
            )

        if payment.status != "pending":
            raise ValueError(
                "Bu payment allaqachon ko'rib chiqilgan."
            )

        payment.status = status

        if admin_note is not None:
            payment.admin_note = admin_note

        async with self.uow:
            return await self.repository.update(
                payment
            )

    async def approve_payment(
        self,
        payment: Payment,
        admin_note: str | None = None,
    ) -> Payment:
        """
        Paymentni tasdiqlaydi.

        Tasdiqlanganda:
        1. Payment pending ekanligi tekshiriladi.
        2. Wallet mavjudligi tekshiriladi.
        3. Payment summasi walletga qo'shiladi.
        4. Payment approved holatiga o'tkaziladi.

        Approve qilingan payment qayta approve qilinmaydi.
        """

        if payment.status != "pending":
            raise ValueError(
                "Bu payment allaqachon ko'rib chiqilgan."
            )

        if payment.amount <= 0:
            raise ValueError(
                "Payment summasi noto'g'ri."
            )

        wallet = await self.wallet_service.get_by_id(
            payment.wallet_id
        )

        if wallet is None:
            raise ValueError(
                "Payment uchun wallet topilmadi."
            )

        await self.wallet_service.add_balance(
            wallet=wallet,
            amount=payment.amount,
            transaction_type="deposit",
            description=(
                f"Payment #{payment.id} approved"
            ),
        )

        payment.status = "approved"

        if admin_note is not None:
            payment.admin_note = admin_note

        async with self.uow:
            return await self.repository.update(
                payment
            )
