from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies.services import get_db_session
from app.modules.admin.services.dashboard_service import DashboardService


router = APIRouter(
    prefix="/admin",
    tags=["Admin Dashboard"],
)


templates = Jinja2Templates(
    directory="app/templates"
)


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    session: AsyncSession = Depends(get_db_session),
):
    service = DashboardService(session)

    stats = await service.get_stats()

    return templates.TemplateResponse(
        request=request,
        name="admin_dashboard.html",
        context={
            "title": "Admin Dashboard",
            "stats": stats,
        },
    )
