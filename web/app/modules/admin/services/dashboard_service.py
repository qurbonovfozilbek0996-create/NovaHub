from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.role import Role
from app.models.permission import Permission

from app.modules.admin.schemas.dashboard import DashboardStats


class DashboardService:
    """
    Admin Dashboard statistikalarini tayyorlaydi.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_stats(self) -> DashboardStats:

        total_roles = await self.session.scalar(
            select(func.count(Role.id))
        )

        total_permissions = await self.session.scalar(
            select(func.count(Permission.id))
        )

        return DashboardStats(
            total_users=0,
            active_users=0,
            total_orders=0,
            pending_orders=0,
            completed_orders=0,
            total_services=0,
            total_platforms=0,
            total_providers=0,
            wallet_balance=0,

            total_roles=total_roles or 0,
            total_permissions=total_permissions or 0,
        )
