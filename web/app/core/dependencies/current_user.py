import json

from fastapi import Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth.auth_context import AuthContext
from app.core.security.security import TelegramWebAppSecurity
from app.modules.users.services.user_service import UserService
from app.services.role_service import RoleService
from app.core.dependencies.services import get_db_session

class CurrentUser:
    """
    NovaHub Current User dependency.

    Telegram WebApp initData orqali foydalanuvchini
    xavfsiz aniqlaydi va AuthContext qaytaradi.
    """

    def __init__(
        self,
        session: AsyncSession,
    ):
        self.users = UserService(session)
        self.roles = RoleService(session)

    async def by_telegram_id(
        self,
        telegram_id: int,
    ) -> AuthContext | None:
        """
        Telegram ID orqali foydalanuvchini topadi.
        """

        user = await self.users.get_by_telegram_id(
            telegram_id
        )

        if user is None:
            return None

        role = None

        if user.role_id is not None:
            role = await self.roles.get_by_id(
                user.role_id
            )

        return AuthContext(
            user=user,
            role=role,
        )

async def get_current_user(
    session: AsyncSession = Depends(get_db_session),
    x_telegram_init_data: str | None = Header(
        default=None,
        alias="X-Telegram-Init-Data",
    ),
) -> AuthContext:
    """
    Telegram WebApp initData orqali current userni aniqlaydi.
    """

    if not x_telegram_init_data:
        raise HTTPException(
            status_code=401,
            detail="Telegram autentifikatsiyasi topilmadi.",
        )

    try:
        data = TelegramWebAppSecurity.validate_init_data(
            x_telegram_init_data
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=401,
            detail=str(exc),
        ) from exc

    raw_user = data.get("user")

    if not raw_user:
        raise HTTPException(
            status_code=401,
            detail="Telegram foydalanuvchi ma'lumoti topilmadi.",
        )

    try:
        telegram_user = json.loads(raw_user)
        telegram_id = int(telegram_user["id"])
    except (
        ValueError,
        TypeError,
        KeyError,
        json.JSONDecodeError,
    ) as exc:
        raise HTTPException(
            status_code=401,
            detail="Telegram foydalanuvchi ma'lumoti noto'g'ri.",
        ) from exc

    current_user = CurrentUser(session)

    auth = await current_user.by_telegram_id(
        telegram_id
    )

    if auth is None:
        raise HTTPException(
            status_code=401,
            detail="Foydalanuvchi NovaHub tizimida topilmadi.",
        )

    if not auth.user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Foydalanuvchi faol emas.",
        )

    if auth.user.is_banned:
        raise HTTPException(
            status_code=403,
            detail="Foydalanuvchi bloklangan.",
        )

    return auth
