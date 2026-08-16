from pydantic import BaseModel, Field

from app.modules.products.models.product import ProductType


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    type: ProductType
    price: int = Field(ge=0)
    is_active: bool = True


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    price: int | None = Field(default=None, ge=0)
    is_active: bool | None = None


class ProductResponse(BaseModel):
    id: int
    name: str
    type: ProductType
    price: int
    is_active: bool

    model_config = {
        "from_attributes": True,
    }
