from aiogram import Router

from app.modules.security.handlers.create_pin import (
    router as create_pin_router,
)
from app.modules.security.handlers.login_pin import (
    router as login_pin_router,
)

security_router = Router(name="security")

security_router.include_router(create_pin_router)
security_router.include_router(login_pin_router)
