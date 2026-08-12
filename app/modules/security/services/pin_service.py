from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.user import User
from app.modules.security.utils.hash import hash_pin, verify_pin


class PinService:
    MAX_ATTEMPTS = 5
    BLOCK_MINUTES = 15

    def __init__(self, db: Session):
        self.db = db

    def create_pin(self, user: User, pin: str) -> None:
        user.pin_hash = hash_pin(pin)
        user.pin_attempts = 0
        user.pin_blocked_until = None
        user.last_login_at = datetime.utcnow()

        self.db.commit()

    def verify(self, user: User, pin: str) -> bool:
        if user.pin_blocked_until:
            if user.pin_blocked_until > datetime.utcnow():
                return False

            user.pin_blocked_until = None
            user.pin_attempts = 0
            self.db.commit()

        if not user.pin_hash:
            return False

        if verify_pin(pin, user.pin_hash):
            user.pin_attempts = 0
            user.last_login_at = datetime.utcnow()
            self.db.commit()
            return True

        user.pin_attempts += 1

        if user.pin_attempts >= self.MAX_ATTEMPTS:
            user.pin_blocked_until = (
                datetime.utcnow() + timedelta(minutes=self.BLOCK_MINUTES)
            )
            user.pin_attempts = 0

        self.db.commit()
        return False

    def is_blocked(self, user: User) -> bool:
        if not user.pin_blocked_until:
            return False

        return user.pin_blocked_until > datetime.utcnow()
