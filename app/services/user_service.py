from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = UserRepository(db)

    def get_by_id(self, user_id: int) -> User | None:
        return self.repository.get_by_id(user_id)

    def get_by_telegram_id(self, telegram_id: int) -> User | None:
        return self.repository.get_by_telegram_id(telegram_id)

    def get_by_phone(self, phone: str) -> User | None:
        return self.repository.get_by_phone(phone)

    def user_exists(self, telegram_id: int) -> bool:
        return self.get_by_telegram_id(telegram_id) is not None

    def create_user(self, **kwargs) -> User:
        return self.repository.create(**kwargs)

    def update_user(self, user: User, **kwargs) -> User:
        return self.repository.update(user, **kwargs)

    def soft_delete(self, user: User) -> None:
        self.repository.soft_delete(user)
