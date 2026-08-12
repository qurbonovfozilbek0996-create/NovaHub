from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.models.wallet import Wallet
from app.models.payment import Payment
from app.models.transaction import Transaction
from app.models.role import Role
from app.models.permission import Permission
from app.models.payment_card import PaymentCard


class DashboardService:
    """
    NovaHub Admin Dashboard statistikalar xizmati.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_statistics(self) -> dict:

        total_users = await self.session.scalar(
            select(func.count(User.id))
        )

        total_wallets = await self.session.scalar(
            select(func.count(Wallet.id))
        )

        pending_payments = await self.session.scalar(
            select(func.count(Payment.id))
            .where(Payment.status == "pending")
        )

        approved_payments = await self.session.scalar(
            select(func.count(Payment.id))
            .where(Payment.status == "approved")
        )

        wallet_turnover = await self.session.scalar(
            select(func.coalesce(func.sum(Transaction.amount), 0))
        )

        total_transactions = await self.session.scalar(
            select(func.count(Transaction.id))
        )

        total_payment_cards = await self.session.scalar(
            select(func.count(PaymentCard.id))
        )

        total_roles = await self.session.scalar(
            select(func.count(Role.id))
        )

        total_permissions = await self.session.scalar(
            select(func.count(Permission.id))
        )

        return {
            "total_users": total_users or 0,
            "total_wallets": total_wallets or 0,
            "pending_payments": pending_payments or 0,
            "approved_payments": approved_payments or 0,
            "wallet_turnover": wallet_turnover or 0,
            "total_transactions": total_transactions or 0,
            "total_payment_cards": total_payment_cards or 0,
            "total_roles": total_roles or 0,
            "total_permissions": total_permissions or 0,
        }
