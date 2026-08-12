from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.permission import Permission
from app.repositories.base_repository import BaseRepository


class PermissionRepository(BaseRepository):
    """
    Permission repository.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_by_id(self, permission_id: int) -> Permission | None:
        result = await self.session.execute(
            select(Permission).where(
                Permission.id == permission_id
            )
        )
        return result.scalar_one_or_none()

    async def get_by_code(
        self,
        code: str,
    ) -> Permission | None:
        result = await self.session.execute(
            select(Permission).where(
                Permission.code == code
            )
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> list[Permission]:
        result = await self.session.execute(
            select(Permission).order_by(
                Permission.module,
                Permission.code,
            )
        )
        return list(result.scalars().all())

    async def create(
        self,
        permission: Permission,
    ) -> Permission:
        self.session.add(permission)
        await self.session.flush()
        await self.session.refresh(permission)
        return permission
