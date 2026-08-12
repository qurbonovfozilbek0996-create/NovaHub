from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies.services import get_db_session
from app.modules.users.services.user_service import UserService


router = APIRouter(
    prefix="/admin/users",
    tags=["Admin Users"],
)


templates = Jinja2Templates(
    directory="app/templates",
)


@router.get("/")
async def list_users(
    page: int = 1,
    per_page: int = 20,
    session: AsyncSession = Depends(get_db_session),
):
    service = UserService(session)

    data = await service.get_users(
        page=page,
        per_page=per_page,
    )

    return {
        "success": True,
        "total": data["total"],
        "page": data["page"],
        "per_page": data["per_page"],
        "users": [
            {
                "id": user.id,
                "telegram_id": user.telegram_id,
                "full_name": user.full_name,
                "username": user.username,
                "role_id": user.role_id,
                "is_active": user.is_active,
                "is_banned": user.is_banned,
            }
            for user in data["items"]
        ],
    }


@router.get(
    "/web",
    response_class=HTMLResponse,
)
async def users_web(
    request: Request,
    session: AsyncSession = Depends(get_db_session),
):
    service = UserService(session)

    data = await service.get_users(
        page=1,
        per_page=100,
    )

    return templates.TemplateResponse(
        request,
        "users/index.html",
        {
            "users": data["items"],
            "page": data["page"],
            "total": data["total"],
        },
    )


@router.get(
    "/{user_id}",
    response_class=HTMLResponse,
)
async def user_detail_web(
    user_id: int,
    request: Request,
    session: AsyncSession = Depends(get_db_session),
):
    service = UserService(session)

    user = await service.get_user(user_id)

    if not user:
        return templates.TemplateResponse(
            request,
            "users/detail.html",
            {
                "user": None,
                "error": "Foydalanuvchi topilmadi.",
            },
            status_code=404,
        )

    return templates.TemplateResponse(
        request,
        "users/detail.html",
        {
            "user": user,
        },
    )


@router.get("/search/{query}")
async def search_users(
    query: str,
    session: AsyncSession = Depends(get_db_session),
):
    service = UserService(session)

    users = await service.search_users(query)

    return {
        "success": True,
        "count": len(users),
        "users": [
            {
                "id": user.id,
                "telegram_id": user.telegram_id,
                "full_name": user.full_name,
                "username": user.username,
                "role_id": user.role_id,
                "is_active": user.is_active,
                "is_banned": user.is_banned,
            }
            for user in users
        ],
    }
