from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.role_permission import RolePermission
from app.models.permission import Permission


class RolePermissionService:
    """
    Role va Permission bog'lanishlarini boshqaradi.
    """

    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_role_permissions(self, role_id: int):
        result = await self.session.execute(
            select(Permission)
            .join(
                RolePermission,
                Permission.id == RolePermission.permission_id,
            )
            .where(
                RolePermission.role_id == role_id,
                RolePermission.is_active == True,
            )
            .order_by(Permission.id)
        )

        return result.scalars().all()


    async def add_permission(
        self,
        role_id: int,
        permission_id: int,
    ):
        existing = await self.session.execute(
            select(RolePermission).where(
                RolePermission.role_id == role_id,
                RolePermission.permission_id == permission_id,
            )
        )

        role_permission = existing.scalar_one_or_none()

        if role_permission:
            if not role_permission.is_active:
                role_permission.is_active = True
                await self.session.commit()

            return role_permission

        role_permission = RolePermission(
            role_id=role_id,
            permission_id=permission_id,
            is_active=True,
        )

        self.session.add(role_permission)

        await self.session.commit()

        return role_permission

    async def remove_permission(
        self,
        role_id: int,
        permission_id: int,
    ):
        result = await self.session.execute(
            select(RolePermission).where(
                RolePermission.role_id == role_id,
                RolePermission.permission_id == permission_id,
            )
        )

        role_permission = result.scalar_one_or_none()

        if not role_permission:
            return False

        role_permission.is_active = False

        await self.session.commit()

        return True
