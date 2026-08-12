from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies.services import get_db_session
from app.modules.platforms.services.platform_service import PlatformService

router = APIRouter(
    prefix="/admin/platforms",
    tags=["Admin Platforms"],
)

templates = Jinja2Templates(directory="app/templates")

@router.get("/")
async def platforms_list(
    only_active: bool = False,
    session: AsyncSession = Depends(get_db_session),
):
    service = PlatformService(session)

    platforms = await service.get_all_platforms(
        only_active=only_active,
    )

    return {
        "success": True,
        "count": len(platforms),
        "items": platforms,
    }

@router.get("/page", response_class=HTMLResponse)
async def platforms_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="platforms/index.html",
        context={"title": "Platformlar"},
    )

@router.get("/{platform_id}")
async def get_platform(
    platform_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    service = PlatformService(session)

    try:
        platform = await service.get_platform(
            platform_id
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

    return {
        "success": True,
        "item": platform,
    }


@router.post("/")
async def create_platform(
    data: dict,
    session: AsyncSession = Depends(get_db_session),
):
    service = PlatformService(session)

    try:
        platform = await service.create_platform(
            name=str(data["name"]),
            slug=str(data["slug"]),
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
        "item": platform,
    }


@router.patch("/{platform_id}/activate")
async def activate_platform(
    platform_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    service = PlatformService(session)

    try:
        platform = await service.activate_platform(
            platform_id
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

    return {
        "success": True,
        "item": platform,
    }


@router.patch("/{platform_id}/deactivate")
async def deactivate_platform(
    platform_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    service = PlatformService(session)

    try:
        platform = await service.deactivate_platform(
            platform_id
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

    return {
        "success": True,
        "item": platform,
    }
