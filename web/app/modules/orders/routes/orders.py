from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies.current_user import get_current_user
from app.core.dependencies.services import get_db_session
from app.modules.orders.services.order_service import OrderService


router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


@router.post("/")
async def create_order(
    data: dict,
    session: AsyncSession = Depends(get_db_session),
    auth=Depends(get_current_user),
):
    required = (
        "service_id",
        "link",
        "quantity",
    )

    for field in required:
        if field not in data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Required field: {field}",
            )

    try:
        order_service = OrderService(session)

        order = await order_service.create_order(
            user_id=auth.user.id,
            service_id=int(data["service_id"]),
            link=str(data["link"]),
            quantity=int(data["quantity"]),
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    return {
        "success": True,
        "message": "Buyurtma yaratildi.",
        "item": {
            "id": order.id,
            "user_id": order.user_id,
            "service_id": order.service_id,
            "provider_id": order.provider_id,
            "link": order.link,
            "quantity": order.quantity,
            "unit_price": float(order.unit_price),
            "total_price": float(order.total_price),
            "status": order.status,
        },
    }
