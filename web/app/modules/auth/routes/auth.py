from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

templates = Jinja2Templates(directory="app/templates")


@router.get(
    "/login",
    response_class=HTMLResponse,
)
async def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="auth/login.html",
        context={
            "title": "NovaHub Login",
        },
    )
