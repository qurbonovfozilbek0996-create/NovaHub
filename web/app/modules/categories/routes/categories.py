from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies.services import get_db_session
from app.modules.categories.services.category_service import (
    CategoryService,
)

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/admin/categories",
    tags=["Admin Categories"],
)

templates = Jinja2Templates(directory="app/templates")

@router.get("/")
async def categories_list(
    platform_id: int | None = None,
    only_active: bool = False,
    session: AsyncSession = Depends(get_db_session),
):
    service = CategoryService(session)

    categories = await service.get_all_categories(
        platform_id=platform_id,
        only_active=only_active,
    )

    return {
        "success": True,
        "count": len(categories),
        "items": categories,
    }

@router.get("/page", response_class=HTMLResponse)
async def categories_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="categories/index.html",
        context={"title": "Kategoriyalar"},
    )

@router.get("/{category_id}")
async def get_category(
    category_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    service = CategoryService(session)

    try:
        category = await service.get_category(
            category_id
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

    return {
        "success": True,
        "item": category,
    }


@router.post("/")
async def create_category(
    data: dict,
    session: AsyncSession = Depends(get_db_session),
):
    service = CategoryService(session)

    try:
        category = await service.create_category(
            name=str(data["name"]),
            platform_id=int(data["platform_id"]),
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
        "item": category,
    }


@router.patch("/{category_id}/activate")
async def activate_category(
    category_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    service = CategoryService(session)

    try:
        category = await service.activate_category(
            category_id
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

    return {
        "success": True,
        "item": category,
    }


@router.patch("/{category_id}/deactivate")
async def deactivate_category(
    category_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    service = CategoryService(session)

    try:
        category = await service.deactivate_category(
            category_id
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

    return {
        "success": True,
        "item": category,
    }
