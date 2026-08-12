from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.core.config.settings import settings
from app.modules.auth.handlers.start import router as start_router
from app.modules.services.handlers.admin.service_handlers import (
    router as service_router,
)

bot = Bot(
    token=settings.BOT_TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML,
    ),
)

dp = Dispatcher()

dp.include_router(start_router)
dp.include_router(service_router)
