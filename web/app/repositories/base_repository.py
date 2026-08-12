from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    """
    NovaHub Base Repository

    Barcha repositorylar uchun asosiy klass.
    """

    def __init__(self, session: AsyncSession):
        self.session = session
