from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.wallet import Wallet


class WalletRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, wallet_id: int):
        return self.db.get(Wallet, wallet_id)

    def get_by_wallet_id(self, wallet_id: str):
        stmt = select(Wallet).where(Wallet.wallet_id == wallet_id)
        return self.db.scalar(stmt)

    def get_by_user_id(self, user_id: int):
        stmt = select(Wallet).where(Wallet.user_id == user_id)
        return self.db.scalar(stmt)

    def create(self, **kwargs):
        wallet = Wallet(**kwargs)
        self.db.add(wallet)
        return wallet

    def update(self, wallet: Wallet, **kwargs):
        for key, value in kwargs.items():
            setattr(wallet, key, value)
        return wallet
