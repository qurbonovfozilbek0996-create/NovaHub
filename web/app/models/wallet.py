from sqlalchemy import (
    BigInteger,
    Boolean,
    ForeignKey,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models.core.base_model import BaseModel


class Wallet(BaseModel):
    """
    NovaHub Wallet

    Har bir foydalanuvchi faqat bitta walletga ega bo'ladi.
    """

    __tablename__ = "wallets"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    wallet_id: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        index=True,
        nullable=False,
    )

    balance: Mapped[int] = mapped_column(
        BigInteger,
        default=0,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    is_locked: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
