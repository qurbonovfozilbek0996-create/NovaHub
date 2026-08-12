from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.core.config.settings import settings
from app.database.session import AsyncSessionLocal
from app.services.seed_service import SeedService

from app.modules.auth.routes.auth import router as auth_router
from app.modules.dashboard.routes.dashboard import router as dashboard_router
from app.modules.admin.routes.payment_cards import router as payment_cards_router
from app.modules.admin.routes.payments import router as admin_payments_router
from app.modules.payments.routes.payments import router as user_payments_router
from app.modules.admin.routes.roles import router as admin_roles_router
from app.modules.admin.routes.permissions import router as admin_permissions_router
from app.modules.admin.routes.role_permissions import (
    router as admin_role_permissions_router,
)
from app.modules.users.routes.users import router as admin_users_router
from app.modules.stars.routes import router as stars_router
from app.modules.services.routes.services import router as services_router
from app.modules.services.routes.user_services import router as user_services_router
from app.modules.services.routes.user_service_detail import router as user_service_detail_router
from app.modules.api_management.routes.providers import (
    router as providers_router,
)
from app.modules.platforms.routes.platforms import (
    router as platforms_router,
)
from app.modules.categories.routes.categories import (
    router as categories_router,
)
from app.modules.admin.routes.dashboard import router as admin_dashboard_router

import app.models

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("NovaHub startup...")

    async with AsyncSessionLocal() as session:
        seed_service = SeedService(session)
        await seed_service.run()

    yield

    print("NovaHub shutdown...")


app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    lifespan=lifespan,
)


app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static",
)


templates = Jinja2Templates(
    directory="app/templates",
)


app.include_router(auth_router)
app.include_router(dashboard_router)

app.include_router(payment_cards_router)
app.include_router(admin_payments_router)
app.include_router(user_payments_router)

app.include_router(admin_roles_router)
app.include_router(admin_permissions_router)
app.include_router(admin_role_permissions_router)
app.include_router(admin_users_router)
app.include_router(admin_dashboard_router)

app.include_router(stars_router)

app.include_router(providers_router)
app.include_router(services_router)
app.include_router(user_services_router)
app.include_router(user_service_detail_router)
app.include_router(platforms_router)
app.include_router(categories_router)

@app.get("/")
async def index():
    return {
        "project": settings.APP_NAME,
        "status": "running",
        "version": "1.0.0",
    }


@app.get("/health")
async def health():
    return {
        "status": "ok",
    }
