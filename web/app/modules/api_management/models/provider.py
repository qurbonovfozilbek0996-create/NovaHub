from datetime import datetime
from enum import Enum

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum as SqlEnum,
    Integer,
    String,
)

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.database.base import Base


class ProviderType(str, Enum):
    SMM = "smm"
    TELEGRAM = "telegram"
    NUMBERS = "numbers"


class Provider(Base):
    __tablename__ = "providers"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    provider_id: Mapped[int] = mapped_column(
        Integer,
        unique=True,
        index=True,
    )

    provider_type: Mapped[ProviderType] = mapped_column(
        SqlEnum(ProviderType),
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(150),
    )

    base_url: Mapped[str] = mapped_column(
        String(500),
    )

    api_key: Mapped[str] = mapped_column(
        String(500),
    )

    api_version: Mapped[str] = mapped_column(
        String(20),
        default="v2",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    priority: Mapped[int] = mapped_column(
        Integer,
        default=1,
    )

    timeout: Mapped[int] = mapped_column(
        Integer,
        default=30,
    )

    last_sync_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    last_error: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
