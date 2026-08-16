from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.products.models.product import Product, ProductType


class ProductService:
    """V1 mahsulotlari bilan ishlash xizmati."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_product(
        self,
        product_type: ProductType,
    ) -> Product | None:
        result = await self.session.execute(
            select(Product).where(
                Product.type == product_type,
            )
        )

        return result.scalar_one_or_none()

    async def get_product_by_id(
        self,
        product_id: int,
    ) -> Product | None:
        result = await self.session.execute(
            select(Product).where(
                Product.id == product_id,
            )
        )

        return result.scalar_one_or_none()

    async def get_all_products(self) -> list[Product]:
        result = await self.session.execute(
            select(Product).order_by(Product.id)
        )

        return list(result.scalars().all())

    async def get_active_products(self) -> list[Product]:
        result = await self.session.execute(
            select(Product)
            .where(Product.is_active.is_(True))
            .order_by(Product.id)
        )

        return list(result.scalars().all())

    async def create_product(
        self,
        name: str,
        product_type: ProductType,
        price: int,
        is_active: bool = True,
    ) -> Product:
        product = Product(
            name=name,
            type=product_type,
            price=price,
            is_active=is_active,
        )

        self.session.add(product)
        await self.session.flush()

        return product

    async def update_product(
        self,
        product: Product,
        *,
        name: str | None = None,
        price: int | None = None,
        is_active: bool | None = None,
    ) -> Product:
        if name is not None:
            product.name = name

        if price is not None:
            product.price = price

        if is_active is not None:
            product.is_active = is_active

        await self.session.flush()

        return product

    async def delete_product(
        self,
        product: Product,
    ) -> None:
        await self.session.delete(product)
        await self.session.flush()
