from sqlalchemy import BigInteger, Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.database.base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        nullable=False,
        index=True,
    )

    full_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    username: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    phone_number: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
    )

    language: Mapped[str] = mapped_column(
        String(10),
        default="uz",
        nullable=False,
    )

    role: Mapped[str] = mapped_column(
        String(30),
        default="user",
        nullable=False,
    )

    is_phone_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_subscribed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    pin_hash: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    pin_attempts: Mapped[int] = mapped_column(
        default=0,
        nullable=False,
    )

    pin_blocked_until: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    wallet = relationship(
        "Wallet",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
