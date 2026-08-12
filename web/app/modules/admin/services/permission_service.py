from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.permission import Permission


class PermissionService:
    """
    Permissionlarni boshqarish servisi.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_permissions(self):
        result = await self.session.execute(
            select(Permission).order_by(
                Permission.module,
                Permission.action,
            )
        )

        return result.scalars().all()
