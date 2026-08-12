from sqlalchemy.orm import Session

from app.models.user import User
from app.models.wallet import Wallet
from app.repositories.user_repository import UserRepository
from app.repositories.wallet_repository import WalletRepository
from app.services.id_generator import generate_wallet_id


class RegistrationService:

    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)
        self.wallet_repository = WalletRepository(db)

    def register_user(
        self,
        telegram_id: int,
        full_name: str,
        username: str | None,
        phone_number: str,
    ) -> tuple[User, Wallet]:

        if self.user_repository.get_by_telegram_id(telegram_id):
            raise ValueError("User already exists")

        try:
            user = self.user_repository.create(
                telegram_id=telegram_id,
                full_name=full_name,
                username=username,
                phone_number=phone_number,
            )

            self.db.flush()

            wallet = self.wallet_repository.create(
                user_id=user.id,
                wallet_id=generate_wallet_id(self.db),
            )

            self.db.flush()

            self.db.commit()

            self.db.refresh(user)
            self.db.refresh(wallet)

            return user, wallet

        except Exception:
            self.db.rollback()
            raise
