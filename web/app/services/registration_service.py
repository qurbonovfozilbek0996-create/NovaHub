from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth.auth_context import AuthContext
from app.core.config.settings import settings
from app.core.uow.unit_of_work import UnitOfWork

from app.models.user import User

from app.services.base_service import BaseService
from app.services.role_service import RoleService
from app.services.user_service import UserService
from app.services.wallet_service import WalletService

class RegistrationService(BaseService):
    """
    NovaHub Registration Service.
    """

    def __init__(
        self,
        session: AsyncSession,
    ):
        super().__init__(session)

        self.users = UserService(session)
        self.roles = RoleService(session)
        self.wallets = WalletService(session)

        self.uow = UnitOfWork(session)

    async def register_telegram_user(
        self,
        telegram_id: int,
        full_name: str,
        username: str | None,
        language: str = "uz",
    ) -> AuthContext:

        existing_user = await self.users.get_by_telegram_id(
            telegram_id
        )

        if existing_user is not None:
            role = None

            if existing_user.role_id is not None:
                role = await self.roles.get_by_id(
                    existing_user.role_id
                )

            return AuthContext(
                user=existing_user,
                role=role,
            )

        role_code = (
            "founder"
            if telegram_id == settings.FOUNDER_TELEGRAM_ID
            else "user"
        )

        role = await self.roles.get_by_code(
            role_code
        )

        async with self.uow:
            user = await self.users.create(
                User(
                    telegram_id=telegram_id,
                    full_name=full_name,
                    username=username,
                    language=language,
                    role_id=role.id if role else None,
                    is_active=True,
                    is_banned=False,
                    referral_count=0,
                )
            )

            await self.wallets.create_wallet(
                user.id
            )

        return AuthContext(
            user=user,
            role=role,
        )
