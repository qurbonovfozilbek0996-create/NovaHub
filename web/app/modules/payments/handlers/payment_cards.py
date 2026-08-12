from fastapi import APIRouter

router = APIRouter(
    prefix="/admin/payment-cards",
    tags=["Admin - Payment Cards"],
)
