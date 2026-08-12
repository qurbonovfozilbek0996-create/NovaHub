from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies.services import get_db_session
from app.modules.services.services.service_service import ServiceService

router = APIRouter(
    tags=["User Services"],
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/services", response_class=HTMLResponse)
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
