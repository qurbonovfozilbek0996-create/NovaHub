from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.core.base_model import BaseModel


class Permission(BaseModel):
    """
    NovaHub tizimidagi ruxsatlar.

    Misollar:
    - users.view
    - users.create
    - wallet.manage
    - support.reply
    """

    __tablename__ = "permissions"

    module: Mapped[str] = mapped_column(
        String(100),
        index=True,
        nullable=False,
    )

    action: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    code: Mapped[str] = mapped_column(
        String(200),
        unique=True,
        index=True,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    is_system: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
