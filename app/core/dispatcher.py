from aiogram import Dispatcher

from app.core.routers import setup_routers
from app.middlewares.database import DatabaseMiddleware

dispatcher = Dispatcher()

dispatcher.update.middleware(DatabaseMiddleware())

setup_routers(dispatcher)
