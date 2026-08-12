from sqlalchemy.orm import Session

from app.models.wallet import Wallet
from app.repositories.wallet_repository import WalletRepository


class WalletService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = WalletRepository(db)

    def get_by_id(self, wallet_id: int) -> Wallet | None:
        return self.repository.get_by_id(wallet_id)

    def get_by_wallet_id(self, wallet_id: str) -> Wallet | None:
        return self.repository.get_by_wallet_id(wallet_id)

    def get_by_user_id(self, user_id: int) -> Wallet | None:
        return self.repository.get_by_user_id(user_id)

    def create(self, **kwargs) -> Wallet:
        return self.repository.create(**kwargs)

    def update(self, wallet: Wallet, **kwargs) -> Wallet:
        return self.repository.update(wallet, **kwargs)
