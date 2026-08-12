from sqlalchemy.ext.asyncio import AsyncSession

from app.database.seeds.seed import DatabaseSeeder
from app.services.base_service import BaseService


class SeedService(BaseService):
    """
    NovaHub Seed Service.

    Database'ni boshlang'ich holatga tayyorlaydi.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.seeder = DatabaseSeeder(session)

    async def run(self) -> None:
        """
        Seed jarayonini ishga tushiradi.
        """
        await self.seeder.run()
        await self.commit()
