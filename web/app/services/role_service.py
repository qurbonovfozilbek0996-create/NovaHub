from sqlalchemy.ext.asyncio import AsyncSession

from app.models.role import Role
from app.repositories.role_repository import RoleRepository
from app.services.base_service import BaseService


class RoleService(BaseService):
    """
    NovaHub Role Service.
    """

    def __init__(
        self,
        session: AsyncSession,
    ):
        super().__init__(session)

        self.roles = RoleRepository(session)

    async def get_by_id(
        self,
        role_id: int,
    ) -> Role | None:
        return await self.roles.get_by_id(role_id)

    async def get_by_code(
        self,
        code: str,
    ) -> Role | None:
        return await self.roles.get_by_code(code)

    async def get_all(
        self,
    ) -> list[Role]:
        return await self.roles.get_all()

    async def create(
        self,
        role: Role,
    ) -> Role:
        return await self.roles.create(role)
