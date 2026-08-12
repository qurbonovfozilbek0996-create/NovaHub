from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies.services import get_db_session
from app.modules.services.services.service_service import ServiceService

router = APIRouter(
    tags=["User Service Detail"],
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/services/{service_id}", response_class=HTMLResponse)
async def user_service_detail(
    service_id: int,
    request: Request,
    session: AsyncSession = Depends(get_db_session),
):
    service = ServiceService(session)

    try:
        item = await service.get_service(service_id)
    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Xizmat topilmadi.",
        )

    if not item.is_active:
        raise HTTPException(
            status_code=404,
            detail="Xizmat hozir mavjud emas.",
        )

    return templates.TemplateResponse(
        request=request,
        name="services/detail.html",
        context={
            "title": item.name,
            "service": item,
        },
    )
