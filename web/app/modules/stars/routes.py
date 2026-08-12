from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/stars", tags=["Telegram Stars"])

templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def stars_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="stars/index.html",
        context={
            "page_title": "Telegram Stars",
        },
    )
