from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.core.base_model import BaseModel


class Payment(BaseModel):
    """
    NovaHub Wallet to'ldirish to'lovlari.
    """

    __tablename__ = "payments"

    wallet_id: Mapped[int] = mapped_column(
        ForeignKey("wallets.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    payment_card_id: Mapped[int | None] = mapped_column(
        ForeignKey("payment_cards.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    amount: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="pending",
        nullable=False,
        index=True,
    )

    receipt_image: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    admin_note: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )
