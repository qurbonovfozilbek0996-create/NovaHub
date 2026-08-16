from enum import Enum

from sqlalchemy import Boolean, Enum as SQLEnum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class ProductType(str, Enum):
    STARS = "stars"
    PREMIUM = "premium"
    GIFT = "gift"


class Product(BaseModel):
    __tablename__ = "products"

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    type: Mapped[ProductType] = mapped_column(
        SQLEnum(ProductType),
        unique=True,
        nullable=False,
    )

    price: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )
