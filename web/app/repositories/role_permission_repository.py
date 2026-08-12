from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.role_permission import RolePermission
from app.repositories.base_repository import BaseRepository


class RolePermissionRepository(BaseRepository):
    """
    Role Permission repository.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get(
        self,
        role_id: int,
        permission_id: int,
    ) -> RolePermission | None:
        result = await self.session.execute(
            select(RolePermission).where(
                RolePermission.role_id == role_id,
                RolePermission.permission_id == permission_id,
            )
        )
        return result.scalar_one_or_none()

    async def get_by_role(
        self,
        role_id: int,
    ) -> list[RolePermission]:
        result = await self.session.execute(
            select(RolePermission).where(
                RolePermission.role_id == role_id
            )
        )
        return list(result.scalars().all())

    async def create(
        self,
        item: RolePermission,
    ) -> RolePermission:
        self.session.add(item)
        await self.session.flush()
        await self.session.refresh(item)
        return item
