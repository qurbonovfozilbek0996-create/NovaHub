from pydantic import Field

from app.schemas.base import BaseSchema

class PaymentCardCreate(BaseSchema):
    card_name: str = Field(..., max_length=100)
    card_number: str = Field(..., max_length=32)
    card_holder: str = Field(..., max_length=255)
    min_amount: int = Field(..., ge=0)
    max_amount: int = Field(..., ge=0)
    payment_note: str | None = Field(default=None, max_length=255)
    qr_image: str | None = Field(default=None, max_length=500)
    sort_order: int = Field(default=1, ge=0)
    is_active: bool = True


class PaymentCardUpdate(BaseSchema):
    card_name: str | None = Field(default=None, max_length=100)
    card_number: str | None = Field(default=None, max_length=32)
    card_holder: str | None = Field(default=None, max_length=255)
    min_amount: int | None = Field(default=None, ge=0)
    max_amount: int | None = Field(default=None, ge=0)
    payment_note: str | None = Field(default=None, max_length=255)
    qr_image: str | None = Field(default=None, max_length=500)
    sort_order: int | None = Field(default=None, ge=0)
    is_active: bool | None = None


class PaymentCardResponse(BaseSchema):
    id: int
    card_name: str
    card_number: str
    card_holder: str
    min_amount: int
    max_amount: int
    payment_note: str | None
    qr_image: str | None
    sort_order: int
    is_active: bool
