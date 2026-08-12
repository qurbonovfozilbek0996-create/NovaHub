from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.platforms.models.platform import Platform


class PlatformService:
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session

    async def create_platform(
        self,
        name: str,
        slug: str,
    ) -> Platform:
        existing = await self.session.scalar(
            select(Platform).where(
                Platform.slug == slug
            )
        )

        if existing:
            raise ValueError(
                "Platform slug already exists."
            )

        platform = Platform(
            name=name.strip(),
            slug=slug.strip(),
            is_active=True,
            sort_order=0,
        )

        self.session.add(platform)

        await self.session.commit()
        await self.session.refresh(platform)

        return platform

    async def get_platform(
        self,
        platform_id: int,
    ) -> Platform:
        platform = await self.session.get(
            Platform,
            platform_id,
        )

        if platform is None:
            raise ValueError(
                "Platform not found."
            )

        return platform

    async def get_all_platforms(
        self,
        only_active: bool = False,
    ) -> list[Platform]:
        query = select(Platform)

        if only_active:
            query = query.where(
                Platform.is_active.is_(True)
            )

        query = query.order_by(
            Platform.sort_order.asc(),
            Platform.name.asc(),
        )

        result = await self.session.scalars(query)

        return list(result.all())

    async def update_platform(
        self,
        platform_id: int,
        **kwargs,
    ) -> Platform:
        platform = await self.get_platform(
            platform_id
        )

        allowed_fields = {
            "name",
            "slug",
            "is_active",
            "sort_order",
        }

        for field, value in kwargs.items():
            if field in allowed_fields:
                setattr(
                    platform,
                    field,
                    value,
                )

        await self.session.commit()
        await self.session.refresh(platform)

        return platform

    async def activate_platform(
        self,
        platform_id: int,
    ) -> Platform:
        platform = await self.get_platform(
            platform_id
        )

        platform.is_active = True

        await self.session.commit()
        await self.session.refresh(platform)

        return platform

    async def deactivate_platform(
        self,
        platform_id: int,
    ) -> Platform:
        platform = await self.get_platform(
            platform_id
        )

        platform.is_active = False

        await self.session.commit()
        await self.session.refresh(platform)

        return platform

    async def delete_platform(
        self,
        platform_id: int,
    ) -> None:
        platform = await self.get_platform(
            platform_id
        )

        await self.session.delete(platform)
        await self.session.commit()
