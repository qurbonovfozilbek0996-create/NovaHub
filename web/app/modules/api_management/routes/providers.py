from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    status,
)

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies.services import get_db_session
from app.modules.api_management.models.provider import ProviderType
from app.modules.api_management.services.provider_service import ProviderService


router = APIRouter(
    prefix="/admin/providers",
    tags=["Admin Providers"],
)


templates = Jinja2Templates(
    directory="app/templates"
)


@router.get("/")
async def providers_list(
    provider_type: ProviderType | None = None,
    only_active: bool = False,
    session: AsyncSession = Depends(get_db_session),
):
    service = ProviderService(session)

    providers = await service.get_all_providers(
        provider_type=provider_type,
        only_active=only_active,
    )

    return {
        "success": True,
        "count": len(providers),
        "items": providers,
    }


@router.get(
    "/page",
    response_class=HTMLResponse,
)
async def providers_page(
    request: Request,
    session: AsyncSession = Depends(get_db_session),
):
    service = ProviderService(session)

    providers = await service.get_all_providers()

    return templates.TemplateResponse(
        request=request,
        name="providers/index.html",
        context={
            "title": "API Providerlar",
            "providers": providers,
        },
    )


@router.get("/{provider_id}")
async def get_provider(
    provider_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    service = ProviderService(session)

    try:
        provider = await service.get_provider(
            provider_id
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

    return {
        "success": True,
        "item": provider,
    }


@router.post("/")
async def create_provider(
    data: dict,
    session: AsyncSession = Depends(get_db_session),
):
    service = ProviderService(session)

    try:
        provider = await service.create_provider(
            provider_id=int(
                data["provider_id"]
            ),
            provider_type=ProviderType(
                data["provider_type"]
            ),
            name=str(
                data["name"]
            ),
            base_url=str(
                data["base_url"]
            ),
            api_key=str(
                data["api_key"]
            ),
            api_version=str(
                data.get(
                    "api_version",
                    "v2",
                )
            ),
            timeout=int(
                data.get(
                    "timeout",
                    30,
                )
            ),
            priority=int(
                data.get(
                    "priority",
                    1,
                )
            ),
        )

    except KeyError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Required field: {exc.args[0]}",
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    return {
        "success": True,
        "item": provider,
    }

@router.patch("/{provider_id}/activate")
async def activate_provider(
    provider_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    service = ProviderService(session)

    try:
        provider = await service.activate_provider(
            provider_id
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    return {
        "success": True,
        "message": "Provider activated successfully.",
        "item": provider,
    }


@router.patch("/{provider_id}/deactivate")
async def deactivate_provider(
    provider_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    service = ProviderService(session)

    try:
        provider = await service.deactivate_provider(
            provider_id
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    return {
        "success": True,
        "message": "Provider deactivated successfully.",
        "item": provider,
    }
