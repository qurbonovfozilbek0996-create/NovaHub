from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.role import Role
from app.repositories.base_repository import BaseRepository


class RoleRepository(BaseRepository):
    """
    Role repository.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_by_id(self, role_id: int) -> Role | None:
        result = await self.session.execute(
            select(Role).where(Role.id == role_id)
        )
        return result.scalar_one_or_none()

    async def get_by_code(self, code: str) -> Role | None:
        result = await self.session.execute(
            select(Role).where(Role.code == code)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> list[Role]:
        result = await self.session.execute(
            select(Role).order_by(Role.id)
        )
        return list(result.scalars().all())

    async def create(self, role: Role) -> Role:
        self.session.add(role)
        await self.session.flush()
        await self.session.refresh(role)
        return role
