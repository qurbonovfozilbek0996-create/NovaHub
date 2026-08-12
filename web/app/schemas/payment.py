from pydantic import Field

from app.schemas.base import BaseSchema


class PaymentCreate(BaseSchema):
    payment_card_id: int | None = None
    amount: int = Field(..., gt=0)
    receipt_image: str | None = Field(
        default=None,
        max_length=500,
    )


class PaymentResponse(BaseSchema):
    id: int
    wallet_id: int
    payment_card_id: int | None
    amount: int
    status: str
    receipt_image: str | None
    admin_note: str | None
