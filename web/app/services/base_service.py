from sqlalchemy.ext.asyncio import AsyncSession


class BaseService:
    """
    NovaHub Base Service.

    Barcha servicelar uchun asosiy klass.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
