from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.api_management.adapters.factory.provider_factory import (
    ProviderFactory,
)
from app.modules.api_management.models.provider import (
    Provider,
    ProviderType,
)


class ProviderService:
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session

    async def create_provider(
        self,
        provider_id: int,
        provider_type: ProviderType,
        name: str,
        base_url: str,
        api_key: str,
        api_version: str = "v2",
        timeout: int = 30,
        priority: int = 1,
    ) -> Provider:

        existing = await self.session.scalar(
            select(Provider).where(
                Provider.provider_id == provider_id
            )
        )

        if existing:
            raise ValueError(
                "Provider ID already exists."
            )

        provider = Provider(
            provider_id=provider_id,
            provider_type=provider_type,
            name=name,
            base_url=base_url.rstrip("/"),
            api_key=api_key,
            api_version=api_version,
            timeout=timeout,
            priority=priority,
            is_active=False,
        )

        self.session.add(provider)

        await self.session.commit()
        await self.session.refresh(provider)

        return provider

    async def update_provider(
        self,
        provider_id: int,
        **kwargs,
    ) -> Provider:

        provider = await self.session.scalar(
            select(Provider).where(
                Provider.provider_id == provider_id
            )
        )

        if provider is None:
            raise ValueError(
                "Provider not found."
            )

        allowed_fields = {
            "name",
            "base_url",
            "api_key",
            "api_version",
            "timeout",
            "priority",
        }

        for field, value in kwargs.items():
            if field not in allowed_fields:
                continue

            if field == "base_url" and isinstance(value, str):
                value = value.rstrip("/")

            setattr(provider, field, value)

        await self.session.commit()
        await self.session.refresh(provider)

        return provider

    async def activate_provider(
        self,
        provider_id: int,
    ) -> Provider:

        provider = await self.session.scalar(
            select(Provider).where(
                Provider.provider_id == provider_id
            )
        )

        if provider is None:
            raise ValueError(
                "Provider not found."
            )

        providers = await self.session.scalars(
            select(Provider).where(
                Provider.provider_type == provider.provider_type
            )
        )

        for item in providers:
            item.is_active = False

        provider.is_active = True

        await self.session.commit()
        await self.session.refresh(provider)

        return provider

    async def deactivate_provider(
        self,
        provider_id: int,
    ) -> Provider:

        provider = await self.session.scalar(
            select(Provider).where(
                Provider.provider_id == provider_id
            )
        )

        if provider is None:
            raise ValueError(
                "Provider not found."
            )

        provider.is_active = False

        await self.session.commit()
        await self.session.refresh(provider)

        return provider

    async def delete_provider(
        self,
        provider_id: int,
    ) -> None:

        provider = await self.session.scalar(
            select(Provider).where(
                Provider.provider_id == provider_id
            )
        )

        if provider is None:
            raise ValueError(
                "Provider not found."
            )

        if provider.is_active:
            raise ValueError(
                "Active provider cannot be deleted."
            )

        await self.session.delete(provider)
        await self.session.commit()

    async def get_provider(
        self,
        provider_id: int,
    ) -> Provider:

        provider = await self.session.scalar(
            select(Provider).where(
                Provider.provider_id == provider_id
            )
        )

        if provider is None:
            raise ValueError(
                "Provider not found."
            )

        return provider

    async def get_all_providers(
        self,
        provider_type: ProviderType | None = None,
        only_active: bool = False,
    ) -> list[Provider]:

        query = select(Provider)

        if provider_type is not None:
            query = query.where(
                Provider.provider_type == provider_type
            )

        if only_active:
            query = query.where(
                Provider.is_active.is_(True)
            )

        query = query.order_by(
            Provider.priority.asc(),
            Provider.name.asc(),
        )

        result = await self.session.scalars(query)

        return list(result.all())

    async def get_active_provider(
        self,
        provider_type: ProviderType,
    ) -> Provider | None:

        return await self.session.scalar(
            select(Provider).where(
                Provider.provider_type == provider_type,
                Provider.is_active.is_(True),
            )
        )

    async def test_connection(
        self,
        provider_id: int,
    ) -> bool:

        provider = await self.get_provider(provider_id)
        adapter = ProviderFactory.create(provider)

        return await adapter.test_connection()

    async def get_balance(
        self,
        provider_id: int,
    ) -> float:

        provider = await self.get_provider(provider_id)
        adapter = ProviderFactory.create(provider)

        return await adapter.get_balance()

    async def sync_services(
        self,
        provider_id: int,
    ) -> list[dict]:
        provider = await self.get_provider(provider_id)

        adapter = ProviderFactory.create(provider)

        services = await adapter.sync_services()

        return services
