from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies.services import get_db_session
from app.services.dashboard_service import DashboardService


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


templates = Jinja2Templates(
    directory="app/templates"
)


@router.get("/", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    session: AsyncSession = Depends(get_db_session),
):
    service = DashboardService(session)

    statistics = await service.get_statistics()

    return templates.TemplateResponse(
        request=request,
        name="dashboard/index.html",
        context={
            "title": "NovaHub",
            "user_name": "Foydalanuvchi",
            "statistics": statistics,
        }
    )
