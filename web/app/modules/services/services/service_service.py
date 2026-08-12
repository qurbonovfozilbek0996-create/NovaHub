from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.services.models.service import Service


class ServiceService:
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session

    async def create_service(
        self,
        service: Service,
    ) -> Service:
        existing = await self.session.scalar(
            select(Service).where(
                Service.service_id == service.service_id
            )
        )

        if existing:
            raise ValueError(
                "Service ID already exists."
            )

        provider_service = await self.session.scalar(
            select(Service).where(
                Service.provider_id == service.provider_id,
                Service.api_service_id == service.api_service_id,
            )
        )

        if provider_service:
            raise ValueError(
                "Service already exists for this provider."
            )

        self.session.add(service)

        await self.session.commit()
        await self.session.refresh(service)

        return service

    async def get_service(
        self,
        service_id: int,
    ) -> Service:
        service = await self.session.get(
            Service,
            service_id,
        )

        if service is None:
            raise ValueError(
                "Service not found."
            )

        return service

    async def get_service_by_api_id(
        self,
        provider_id: int,
        api_service_id: str,
    ) -> Service | None:
        return await self.session.scalar(
            select(Service).where(
                Service.provider_id == provider_id,
                Service.api_service_id == api_service_id,
            )
        )

    async def get_all_services(
        self,
        platform_id: int | None = None,
        category_id: int | None = None,
        provider_id: int | None = None,
        only_active: bool = False,
    ) -> list[Service]:
        query = select(Service)

        if platform_id is not None:
            query = query.where(
                Service.platform_id == platform_id
            )

        if category_id is not None:
            query = query.where(
                Service.category_id == category_id
            )

        if provider_id is not None:
            query = query.where(
                Service.provider_id == provider_id
            )

        if only_active:
            query = query.where(
                Service.is_active.is_(True)
            )

        query = query.order_by(
            Service.sort_order.asc(),
            Service.name.asc(),
        )

        result = await self.session.scalars(query)

        return list(result.all())

    async def update_service(
        self,
        service_id: int,
        **kwargs,
    ) -> Service:
        service = await self.get_service(service_id)

        allowed_fields = {
            "name",
            "description",
            "platform_id",
            "category_id",
            "api_service_id",
            "api_price",
            "sale_price",
            "min_quantity",
            "max_quantity",
            "markup_percent",
            "is_active",
            "is_featured",
            "sort_order",
            "synced_at",
        }

        for field, value in kwargs.items():
            if field in allowed_fields:
                setattr(service, field, value)

        await self.session.commit()
        await self.session.refresh(service)

        return service

    async def activate_service(
        self,
        service_id: int,
    ) -> Service:
        service = await self.get_service(service_id)

        service.is_active = True

        await self.session.commit()
        await self.session.refresh(service)

        return service

    async def deactivate_service(
        self,
        service_id: int,
    ) -> Service:
        service = await self.get_service(service_id)

        service.is_active = False

        await self.session.commit()
        await self.session.refresh(service)

        return service

    async def feature_service(
        self,
        service_id: int,
    ) -> Service:
        service = await self.get_service(service_id)

        service.is_featured = True

        await self.session.commit()
        await self.session.refresh(service)

        return service

    async def unfeature_service(
        self,
        service_id: int,
    ) -> Service:
        service = await self.get_service(service_id)

        service.is_featured = False

        await self.session.commit()
        await self.session.refresh(service)

        return service

    async def delete_service(
        self,
        service_id: int,
    ) -> None:
        service = await self.get_service(service_id)

        await self.session.delete(service)
        await self.session.commit()

    async def sync_service(
        self,
        service: Service,
        api_data: dict,
    ) -> Service:
        """
        API bilan sinxronlash.

        API ma'lumotlari:
        - api_name
        - api_price
        - min_quantity
        - max_quantity

        NovaHub admin ma'lumotlari:
        - name
        - description
        - sale_price

        API sync admin tomonidan o'zgartirilgan
        NovaHub ma'lumotlarini bosib ketmaydi.
        """

        # ---------------------------------------------------------
        # 1. API'DAGI ASL XIZMAT NOMI
        # ---------------------------------------------------------
        api_name = api_data.get("name")

        if api_name is not None:
            service.api_name = str(api_name)

        # ---------------------------------------------------------
        # 2. NOVAHUB NOMI
        # ---------------------------------------------------------
        # Admin o'zi nom bergan bo'lsa, API sync uni o'zgartirmaydi.
        #
        # Faqat NovaHub nomi hali bo'sh bo'lsa,
        # API nomidan boshlang'ich nom sifatida foydalanamiz.
        if not service.name and api_name:
            service.name = str(api_name)

        # ---------------------------------------------------------
        # 3. API NARXI
        # ---------------------------------------------------------
        # Tannarx API'dan doimo yangilanadi.
        if api_data.get("rate") is not None:
            service.api_price = api_data["rate"]

        # ---------------------------------------------------------
        # 4. MINIMAL MIQDOR
        # ---------------------------------------------------------
        if api_data.get("min") is not None:
            service.min_quantity = api_data["min"]

        # ---------------------------------------------------------
        # 5. MAKSIMAL MIQDOR
        # ---------------------------------------------------------
        if api_data.get("max") is not None:
            service.max_quantity = api_data["max"]

        # ---------------------------------------------------------
        # 6. TAVSIF
        # ---------------------------------------------------------
        # API tavsifi mavjud bo'lsa va NovaHub tavsifi
        # hali bo'sh bo'lsa, boshlang'ich tavsif sifatida olamiz.
        #
        # Keyinchalik admin tahrirlasa API sync uni o'zgartirmaydi.
        if not service.description:
            api_description = api_data.get("description")

            if api_description:
                service.description = str(api_description)

        # ---------------------------------------------------------
        # 7. SOTUV NARXI
        # ---------------------------------------------------------
        # sale_price API'dan olinmaydi.
        #
        # Bu NovaHub'ning o'z narxi.
        # Admin o'zi belgilaydi.
        #
        # API sync bu qiymatga TEGMAYDI.

        # ---------------------------------------------------------
        # 8. SINXRONLASH VAQTI
        # ---------------------------------------------------------
        service.synced_at = datetime.utcnow()

        await self.session.commit()
        await self.session.refresh(service)

        return service
