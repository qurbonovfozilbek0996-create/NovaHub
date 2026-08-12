from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.services.base_service import BaseService


class UserService(BaseService):
    """
    NovaHub User Service.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.users = UserRepository(session)

    async def get_by_id(self, user_id: int) -> User | None:
        return await self.users.get_by_id(user_id)

    async def get_by_telegram_id(
        self,
        telegram_id: int,
    ) -> User | None:
        return await self.users.get_by_telegram_id(
            telegram_id
        )

    async def create(
        self,
        user: User,
    ) -> User:
        return await self.users.create(user)

    async def save(self) -> None:
        await self.commit()
