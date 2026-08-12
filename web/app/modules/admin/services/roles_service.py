from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.role import Role


class RolesService:
    """
    Admin roles boshqaruvi.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_roles(self):
        result = await self.session.execute(
            select(Role)
            .order_by(Role.id)
        )

        return result.scalars().all()

    async def get_role(self, role_id: int):
        result = await self.session.execute(
            select(Role)
            .where(Role.id == role_id)
        )

        return result.scalar_one_or_none()

    async def get_role_permissions(self, role_id: int):
        from app.models.role_permission import RolePermission
        from app.models.permission import Permission

        result = await self.session.execute(
            select(Permission)
            .join(
                RolePermission,
                Permission.id == RolePermission.permission_id
            )
            .where(
                RolePermission.role_id == role_id,
                RolePermission.is_active == True
            )
        )

        return result.scalars().all()
