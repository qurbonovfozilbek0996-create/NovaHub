from sqlalchemy import BigInteger, Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.core.base_model import BaseModel


class PaymentCard(BaseModel):
    """
    NovaHub to'lov kartalari.

    Admin panel orqali boshqariladi.
    """

    __tablename__ = "payment_cards"

    card_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    card_number: Mapped[str] = mapped_column(
        String(32),
        unique=True,
        nullable=False,
        index=True,
    )

    card_holder: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    min_amount: Mapped[int] = mapped_column(
        BigInteger,
        default=1000,
        nullable=False,
    )

    max_amount: Mapped[int] = mapped_column(
        BigInteger,
        default=1000000,
        nullable=False,
    )

    payment_note: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    qr_image: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    sort_order: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
