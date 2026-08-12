from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.api_management.services.provider_service import ProviderService
from app.modules.services.models.service import Service
from app.modules.services.services.service_service import ServiceService


class ServiceSyncService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.provider_service = ProviderService(session)
        self.service_service = ServiceService(session)

    async def sync_provider_services(
        self,
        provider_id: int,
        platform_id: int,
        category_id: int,
    ) -> list[Service]:
        api_services = await self.provider_service.sync_services(provider_id)
        synced_services = []

        for data in api_services:
            if not self._valid(data):
                continue

            api_id = str(data["service"])
            service = await self.service_service.get_service_by_api_id(
                provider_id, api_id
            )

            if service is None:
                service = await self._create(
                    provider_id, platform_id, category_id, data
                )
            else:
                service.platform_id = platform_id
                service.category_id = category_id
                service = await self.service_service.sync_service(service, data)

            synced_services.append(service)

        return synced_services

    @staticmethod
    def _valid(data: dict[str, Any]) -> bool:
        try:
            return (
                data.get("service") is not None
                and bool(str(data.get("name") or "").strip())
                and int(data["service"]) > 0
            )
        except (TypeError, ValueError):
            return False

    async def _create(
        self,
        provider_id: int,
        platform_id: int,
        category_id: int,
        data: dict[str, Any],
    ) -> Service:
        api_id = str(data["service"])
        api_name = str(data.get("name") or "").strip()

        service = Service(
            service_id=int(api_id),
            name=api_name,
            api_name=api_name,
            platform_id=platform_id,
            category_id=category_id,
            provider_id=provider_id,
            api_service_id=api_id,
            api_price=self._float(data.get("rate")),
            min_quantity=self._int(data.get("min")),
            max_quantity=self._int(data.get("max")),
            markup_percent=0,
            sale_price=0,
            is_active=False,
            is_featured=False,
            sort_order=0,
        )

        return await self.service_service.create_service(service)

    @staticmethod
    def _int(value: Any) -> int:
        try:
            return int(value or 0)
        except (TypeError, ValueError):
            return 0

    @staticmethod
    def _float(value: Any) -> float:
        try:
            return float(value or 0)
        except (TypeError, ValueError):
            return 0
