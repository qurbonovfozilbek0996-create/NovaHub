from aiogram import Router

from app.modules.auth.handlers.start import router as start_router
from app.modules.auth.handlers.register import router as register_router

router = Router(name="auth")

router.include_router(start_router)

router.include_router(register_router)
