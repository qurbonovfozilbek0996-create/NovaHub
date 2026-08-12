from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int):
        return self.db.get(User, user_id)

    def get_by_telegram_id(self, telegram_id: int):
        stmt = select(User).where(User.telegram_id == telegram_id)
        return self.db.scalar(stmt)

    def get_by_phone(self, phone: str):
        stmt = select(User).where(User.phone_number == phone)
        return self.db.scalar(stmt)

    def create(self, **kwargs):
        user = User(**kwargs)
        self.db.add(user)
        return user

    def update(self, user: User, **kwargs):
        for key, value in kwargs.items():
            setattr(user, key, value)

        return user

    def soft_delete(self, user: User):
        user.status = "deleted"
