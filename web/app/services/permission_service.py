from sqlalchemy.ext.asyncio import AsyncSession

from app.models.permission import Permission
from app.repositories.permission_repository import PermissionRepository
from app.services.base_service import BaseService


class PermissionService(BaseService):
    """
    NovaHub Permission Service.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.permissions = PermissionRepository(session)

    async def get_by_code(
        self,
        code: str,
    ) -> Permission | None:
        return await self.permissions.get_by_code(code)

    async def get_all(self) -> list[Permission]:
        return await self.permissions.get_all()

    async def create(
        self,
        permission: Permission,
    ) -> Permission:
        return await self.permissions.create(permission)
