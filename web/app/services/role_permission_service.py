from sqlalchemy.ext.asyncio import AsyncSession

from app.models.role_permission import RolePermission
from app.repositories.role_permission_repository import (
    RolePermissionRepository,
)
from app.services.base_service import BaseService


class RolePermissionService(BaseService):
    """
    Role Permission Service.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.role_permissions = RolePermissionRepository(session)

    async def get(
        self,
        role_id: int,
        permission_id: int,
    ) -> RolePermission | None:
        return await self.role_permissions.get(
            role_id,
            permission_id,
        )

    async def create(
        self,
        item: RolePermission,
    ) -> RolePermission:
        return await self.role_permissions.create(item)
