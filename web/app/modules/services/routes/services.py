from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies.services import get_db_session
from app.modules.api_management.services.provider_service import ProviderService
from app.modules.services.models.service import Service
from app.modules.services.services.service_service import ServiceService


templates = Jinja2Templates(directory="app/templates")

router = APIRouter(
    prefix="/admin/services",
    tags=["Admin Services"],
)


@router.get("/new", response_class=HTMLResponse)
async def new_service_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="services/new.html",
        context={"title": "Xizmat qo‘shish"},
    )


@router.get("/api-services")
async def api_services(
    provider_id: int = Query(...),
    session: AsyncSession = Depends(get_db_session),
):
    try:
        provider_service = ProviderService(session)
        services = await provider_service.sync_services(provider_id)

        result = []

        for item in services:
            if not isinstance(item, dict):
                continue

            service_id = item.get("service")
            name = item.get("name")

            if service_id is None or not name:
                continue

            result.append(
                {
                    "service_id": int(service_id),
                    "api_service_id": str(service_id),
                    "api_name": str(name),
                    "api_price": float(item.get("rate") or 0),
                    "min_quantity": int(item.get("min") or 0),
                    "max_quantity": int(item.get("max") or 0),
                }
            )

        return {
            "success": True,
            "count": len(result),
            "items": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"API xizmatlarini olishda xatolik: {exc}",
        )


@router.get("/")
async def services_list(
    platform_id: int | None = Query(default=None),
    category_id: int | None = Query(default=None),
    provider_id: int | None = Query(default=None),
    only_active: bool = Query(default=False),
    session: AsyncSession = Depends(get_db_session),
):
    service = ServiceService(session)

    services = await service.get_all_services(
        platform_id=platform_id,
        category_id=category_id,
        provider_id=provider_id,
        only_active=only_active,
    )

    return {
        "success": True,
        "count": len(services),
        "items": services,
    }


@router.get("/page", response_class=HTMLResponse)
async def services_page(
    request: Request,
    session: AsyncSession = Depends(get_db_session),
):
    service = ServiceService(session)
    services = await service.get_all_services()

    return templates.TemplateResponse(
        request=request,
        name="services/index.html",
        context={
            "title": "Xizmatlar",
            "services": services,
        },
    )

@router.get("/user", response_class=HTMLResponse)
async def user_services_page(
    request: Request,
    session: AsyncSession = Depends(get_db_session),
):
    service = ServiceService(session)

    services = await service.get_all_services(
        only_active=True,
    )

    return templates.TemplateResponse(
        request=request,
        name="services/user.html",
        context={
            "title": "Xizmatlar",
            "services": services,
        },
    )

@router.get("/{service_id}")
async def get_service(
    service_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    service = ServiceService(session)

    try:
        item = await service.get_service(service_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

    return {
        "success": True,
        "item": item,
    }


@router.post("/")
async def create_service(
    data: dict,
    session: AsyncSession = Depends(get_db_session),
):
    required = (
        "service_id",
        "name",
        "platform_id",
        "category_id",
        "provider_id",
        "api_service_id",
    )

    for field in required:
        if field not in data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Required field: {field}",
            )

    service = ServiceService(session)

    item = Service(
        service_id=int(data["service_id"]),
        name=str(data["name"]).strip(),
        api_name=(
            str(data["api_name"]).strip()
            if data.get("api_name")
            else None
        ),
        platform_id=int(data["platform_id"]),
        category_id=int(data["category_id"]),
        provider_id=int(data["provider_id"]),
        api_service_id=str(data["api_service_id"]),
        api_price=float(data.get("api_price") or 0),
        sale_price=float(data.get("sale_price") or 0),
        min_quantity=int(data.get("min_quantity") or 0),
        max_quantity=int(data.get("max_quantity") or 0),
        markup_percent=float(data.get("markup_percent") or 0),
        is_active=bool(data.get("is_active", False)),
        is_featured=False,
        sort_order=int(data.get("sort_order") or 0),
    )

    try:
        created = await service.create_service(item)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    return {
        "success": True,
        "item": created,
    }


@router.put("/{service_id}")
async def update_service(
    service_id: int,
    data: dict,
    session: AsyncSession = Depends(get_db_session),
):
    service = ServiceService(session)

    try:
        item = await service.update_service(
            service_id,
            **data,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

    return {
        "success": True,
        "item": item,
    }


@router.delete("/{service_id}")
async def delete_service(
    service_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    service = ServiceService(session)

    try:
        await service.delete_service(service_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

    return {
        "success": True,
        "message": "Service deleted.",
    }


@router.patch("/{service_id}/activate")
async def activate_service(
    service_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    service = ServiceService(session)

    try:
        item = await service.activate_service(service_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

    return {
        "success": True,
        "item": item,
    }


@router.patch("/{service_id}/deactivate")
async def deactivate_service(
    service_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    service = ServiceService(session)

    try:
        item = await service.deactivate_service(service_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

    return {
        "success": True,
        "item": item,
    }
