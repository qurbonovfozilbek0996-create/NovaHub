from sqlalchemy import ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel


class Transaction(BaseModel):
    __tablename__ = "transactions"

    wallet_id: Mapped[int] = mapped_column(
        ForeignKey("wallets.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    transaction_id: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
        index=True,
    )

    transaction_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    amount: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
    )

    balance_before: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
    )

    balance_after: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
    )

    reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    approved_by: Mapped[int | None] = mapped_column(
        nullable=True,
    )

    wallet = relationship(
        "Wallet",
        back_populates="transactions",
    )
