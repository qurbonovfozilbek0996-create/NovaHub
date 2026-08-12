from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_permission import UserPermission
from app.repositories.user_permission_repository import (
    UserPermissionRepository,
)
from app.services.base_service import BaseService


class UserPermissionService(BaseService):
    """
    User Permission Service.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.user_permissions = UserPermissionRepository(session)

    async def get(
        self,
        user_id: int,
        permission_id: int,
    ) -> UserPermission | None:
        return await self.user_permissions.get(
            user_id,
            permission_id,
        )

    async def create(
        self,
        item: UserPermission,
    ) -> UserPermission:
        return await self.user_permissions.create(item)
