from sqlalchemy import BigInteger, Numeric, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel


class Wallet(BaseModel):
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
        nullable=False,
        index=True,
    )

    balance: Mapped[float] = mapped_column(
        Numeric(18, 2),
        default=0,
        nullable=False,
    )

    frozen_balance: Mapped[float] = mapped_column(
        Numeric(18, 2),
        default=0,
        nullable=False,
    )

    currency: Mapped[str] = mapped_column(
        String(5),
        default="UZS",
        nullable=False,
    )

    total_deposit: Mapped[float] = mapped_column(
        Numeric(18, 2),
        default=0,
        nullable=False,
    )

    total_spent: Mapped[float] = mapped_column(
        Numeric(18, 2),
        default=0,
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="wallet",
    )

    transactions = relationship(
        "Transaction",
        back_populates="wallet",
        cascade="all, delete-orphan",
    )
