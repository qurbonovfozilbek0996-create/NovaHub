from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.categories.models.category import Category


class CategoryService:
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session

    async def create_category(
        self,
        name: str,
        platform_id: int,
    ) -> Category:
        platform_exists = await self.session.scalar(
            select(Category).where(
                Category.platform_id == platform_id,
                Category.name == name.strip(),
            )
        )

        if platform_exists:
            raise ValueError(
                "Category already exists for this platform."
            )

        category = Category(
            name=name.strip(),
            platform_id=platform_id,
            is_active=True,
            sort_order=0,
        )

        self.session.add(category)

        await self.session.commit()
        await self.session.refresh(category)

        return category

    async def get_category(
        self,
        category_id: int,
    ) -> Category:
        category = await self.session.get(
            Category,
            category_id,
        )

        if category is None:
            raise ValueError(
                "Category not found."
            )

        return category

    async def get_all_categories(
        self,
        platform_id: int | None = None,
        only_active: bool = False,
    ) -> list[Category]:
        query = select(Category)

        if platform_id is not None:
            query = query.where(
                Category.platform_id == platform_id
            )

        if only_active:
            query = query.where(
                Category.is_active.is_(True)
            )

        query = query.order_by(
            Category.sort_order.asc(),
            Category.name.asc(),
        )

        result = await self.session.scalars(query)

        return list(result.all())

    async def update_category(
        self,
        category_id: int,
        **kwargs,
    ) -> Category:
        category = await self.get_category(
            category_id
        )

        allowed_fields = {
            "name",
            "platform_id",
            "is_active",
            "sort_order",
        }

        for field, value in kwargs.items():
            if field in allowed_fields:
                setattr(
                    category,
                    field,
                    value,
                )

        await self.session.commit()
        await self.session.refresh(category)

        return category

    async def activate_category(
        self,
        category_id: int,
    ) -> Category:
        category = await self.get_category(
            category_id
        )

        category.is_active = True

        await self.session.commit()
        await self.session.refresh(category)

        return category

    async def deactivate_category(
        self,
        category_id: int,
    ) -> Category:
        category = await self.get_category(
            category_id
        )

        category.is_active = False

        await self.session.commit()
        await self.session.refresh(category)

        return category

    async def delete_category(
        self,
        category_id: int,
    ) -> None:
        category = await self.get_category(
            category_id
        )

        await self.session.delete(category)
        await self.session.commit()
