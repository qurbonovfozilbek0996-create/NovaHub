from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)

from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Service(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    # API dagi asl xizmat ID
    service_id: Mapped[int] = mapped_column(
        Integer,
        unique=True,
        index=True,
    )

    # NovaHub ichida ko‘rinadigan nom
    # API dagi nomdan mustaqil
    name: Mapped[str] = mapped_column(
        String(255),
    )

    # API dagi asl nom
    # Keyinchalik API sinxronlashda NovaHub nomi o‘zgarmaydi
    api_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    # NovaHub ichida ko‘rinadigan tavsif
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    platform_id: Mapped[int] = mapped_column(
        ForeignKey("platforms.id"),
        index=True,
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"),
        index=True,
    )

    provider_id: Mapped[int] = mapped_column(
        ForeignKey("providers.id"),
        index=True,
    )

    # Provider API dagi xizmat ID
    api_service_id: Mapped[str] = mapped_column(
        String(100),
        index=True,
    )

    # Providerdan keladigan tannarx
    api_price: Mapped[float] = mapped_column(
        Numeric(18, 6),
        default=0,
    )

    # NovaHubdagi sotuv narxi
    sale_price: Mapped[float] = mapped_column(
        Numeric(18, 6),
        default=0,
    )

    min_quantity: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    max_quantity: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    # Eski ustama tizimi saqlanadi
    markup_percent: Mapped[float] = mapped_column(
        Numeric(5, 2),
        default=0,
    )

    # Sotuvga chiqarilganmi?
    # False = sotuvda emas
    # True = sotuvda
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    is_featured: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    sort_order: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    # API bilan oxirgi sinxronlash vaqti
    synced_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
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
