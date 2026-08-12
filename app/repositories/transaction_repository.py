from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.transaction import Transaction


class TransactionRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, transaction_id: int):
        return self.db.get(Transaction, transaction_id)

    def get_by_transaction_id(self, transaction_id: str):
        stmt = select(Transaction).where(
            Transaction.transaction_id == transaction_id
        )
        return self.db.scalar(stmt)

    def get_by_wallet_id(self, wallet_id: int):
        stmt = select(Transaction).where(
            Transaction.wallet_id == wallet_id
        )
        return self.db.scalars(stmt).all()

    def create(self, **kwargs):
        transaction = Transaction(**kwargs)
        self.db.add(transaction)
        return transaction
