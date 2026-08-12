from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_session():
        yield session
