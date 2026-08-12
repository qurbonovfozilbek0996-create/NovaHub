from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class PromotionTarget(Base):
    __tablename__ = "promotion_targets"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    promotion_id: Mapped[int] = mapped_column(
        ForeignKey("promotions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    target_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    target_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True,
    )
