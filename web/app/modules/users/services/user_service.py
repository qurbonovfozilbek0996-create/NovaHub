from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserService:
    """
    NovaHub foydalanuvchilarini boshqarish servisi.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_users(
        self,
        page: int = 1,
        per_page: int = 20,
    ):
        """
        Foydalanuvchilar ro‘yxatini sahifalash bilan qaytaradi.
        """

        if page < 1:
            page = 1

        if per_page < 1:
            per_page = 20

        offset = (page - 1) * per_page

        result = await self.session.execute(
            select(User)
            .order_by(User.id.desc())
            .offset(offset)
            .limit(per_page)
        )

        total = await self.session.scalar(
            select(func.count(User.id))
        )

        return {
            "items": result.scalars().all(),
            "total": total or 0,
            "page": page,
            "per_page": per_page,
        }

    async def get_user(
        self,
        user_id: int,
    ):
        """
        ID orqali bitta foydalanuvchini topadi.
        """

        result = await self.session.execute(
            select(User).where(
                User.id == user_id,
            )
        )

        return result.scalar_one_or_none()

    async def search_users(
        self,
        query: str,
    ):
        """
        Ism yoki username orqali foydalanuvchilarni qidiradi.
        """

        query = query.strip()

        if not query:
            return []

        result = await self.session.execute(
            select(User)
            .where(
                (User.full_name.ilike(f"%{query}%"))
                | (User.username.ilike(f"%{query}%"))
            )
            .order_by(User.id.desc())
        )

        return result.scalars().all()

    async def get_by_telegram_id(
        self,
        telegram_id: int,
    ):
        """
        Telegram ID orqali foydalanuvchini topadi.
        """

        result = await self.session.execute(
            select(User).where(
                User.telegram_id == telegram_id,
            )
        )

        return result.scalar_one_or_none()
