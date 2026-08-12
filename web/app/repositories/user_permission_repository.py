from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_permission import UserPermission
from app.repositories.base_repository import BaseRepository


class UserPermissionRepository(BaseRepository):
    """
    User Permission repository.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get(
        self,
        user_id: int,
        permission_id: int,
    ) -> UserPermission | None:
        result = await self.session.execute(
            select(UserPermission).where(
                UserPermission.user_id == user_id,
                UserPermission.permission_id == permission_id,
            )
        )
        return result.scalar_one_or_none()

    async def get_by_user(
        self,
        user_id: int,
    ) -> list[UserPermission]:
        result = await self.session.execute(
            select(UserPermission).where(
                UserPermission.user_id == user_id
            )
        )
        return list(result.scalars().all())

    async def create(
        self,
        item: UserPermission,
    ) -> UserPermission:
        self.session.add(item)
        await self.session.flush()
        await self.session.refresh(item)
        return item
