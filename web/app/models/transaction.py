from sqlalchemy import (
    BigInteger,
    Boolean,
    ForeignKey,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models.core.base_model import BaseModel


class Transaction(BaseModel):
    """
    NovaHub moliyaviy operatsiyalari.
    """

    __tablename__ = "transactions"

    transaction_id: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        index=True,
        nullable=False,
    )

    wallet_id: Mapped[int] = mapped_column(
        ForeignKey("wallets.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    sender_wallet_id: Mapped[int | None] = mapped_column(
        ForeignKey("wallets.id", ondelete="SET NULL"),
        nullable=True,
    )

    receiver_wallet_id: Mapped[int | None] = mapped_column(
        ForeignKey("wallets.id", ondelete="SET NULL"),
        nullable=True,
    )

    type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        index=True,
    )

    amount: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    commission: Mapped[int] = mapped_column(
        BigInteger,
        default=0,
        nullable=False,
    )

    cashback: Mapped[int] = mapped_column(
        BigInteger,
        default=0,
        nullable=False,
    )

    balance_before: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    balance_after: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    is_reversed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
