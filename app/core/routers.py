from aiogram import Dispatcher

from app.modules.auth.routers import router as auth_router
from app.modules.common.routers import router as common_router
from app.modules.security.routers import security_router

def setup_routers(dp: Dispatcher) -> None:
    """
    Bu yerga barcha modullar routerlari ulanadi.
    """
    dp.include_router(auth_router)

    dp.include_router(common_router)

    dp.include_router(security_router)
