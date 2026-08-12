from aiogram import Router

from app.modules.common.handlers.menu import router as menu_router

router = Router(name="common")

router.include_router(menu_router)
