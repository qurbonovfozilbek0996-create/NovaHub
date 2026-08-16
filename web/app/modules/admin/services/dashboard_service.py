from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.permission import Permission
from app.models.role import Role
from app.models.user import User
from app.models.wallet import Wallet

from app.modules.admin.schemas.dashboard import DashboardStats
from app.modules.api_management.models.provider import Provider
from app.modules.orders.models.order import Order
from app.modules.platforms.models.platform import Platform
from app.modules.services.models.service import Service


class DashboardService:
    """
    Admin Dashboard statistikalarini tayyorlaydi.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_stats(self) -> DashboardStats:
        total_users = await self.session.scalar(
            select(func.count(User.id))
        )

        active_users = await self.session.scalar(
            select(func.count(User.id)).where(
                User.is_active.is_(True),
                User.is_banned.is_(False),
            )
        )

        total_orders = await self.session.scalar(
            select(func.count(Order.id))
        )

        pending_orders = await self.session.scalar(
            select(func.count(Order.id)).where(
                Order.status == "pending"
            )
        )

        completed_orders = await self.session.scalar(
            select(func.count(Order.id)).where(
                Order.status == "completed"
            )
        )

        total_services = await self.session.scalar(
            select(func.count(Service.id))
        )

        total_platforms = await self.session.scalar(
            select(func.count(Platform.id))
        )

        total_providers = await self.session.scalar(
            select(func.count(Provider.id))
        )

        wallet_balance = await self.session.scalar(
            select(func.coalesce(func.sum(Wallet.balance), 0))
        )

        total_roles = await self.session.scalar(
            select(func.count(Role.id))
        )

        total_permissions = await self.session.scalar(
            select(func.count(Permission.id))
        )

        return DashboardStats(
            total_users=total_users or 0,
            active_users=active_users or 0,
            total_orders=total_orders or 0,
            pending_orders=pending_orders or 0,
            completed_orders=completed_orders or 0,
            total_services=total_services or 0,
            total_platforms=total_platforms or 0,
            total_providers=total_providers or 0,
            wallet_balance=wallet_balance or 0,
            total_roles=total_roles or 0,
            total_permissions=total_permissions or 0,
        )
