from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies.services import get_db_session
from app.modules.products.schemas import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
)
from app.modules.products.services import ProductService


router = APIRouter(
    prefix="/admin/products",
    tags=["Admin Products"],
)


@router.get(
    "/",
    response_model=list[ProductResponse],
)
async def products_list(
    session: AsyncSession = Depends(get_db_session),
):
    service = ProductService(session)

    return await service.get_all_products()


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
)
async def product_detail(
    product_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    service = ProductService(session)

    product = await service.get_product_by_id(product_id)

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mahsulot topilmadi.",
        )

    return product


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    data: ProductCreate,
    session: AsyncSession = Depends(get_db_session),
):
    service = ProductService(session)

    existing = await service.get_product(data.type)

    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Bu turdagi mahsulot allaqachon mavjud.",
        )

    product = await service.create_product(
        name=data.name,
        product_type=data.type,
        price=data.price,
        is_active=data.is_active,
    )

    await session.commit()
    await session.refresh(product)

    return product


@router.put(
    "/{product_id}",
    response_model=ProductResponse,
)
async def update_product(
    product_id: int,
    data: ProductUpdate,
    session: AsyncSession = Depends(get_db_session),
):
    service = ProductService(session)

    product = await service.get_product_by_id(product_id)

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mahsulot topilmadi.",
        )

    product = await service.update_product(
        product,
        name=data.name,
        price=data.price,
        is_active=data.is_active,
    )

    await session.commit()
    await session.refresh(product)

    return product


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_product(
    product_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    service = ProductService(session)

    product = await service.get_product_by_id(product_id)

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mahsulot topilmadi.",
        )

    await service.delete_product(product)
    await session.commit()
