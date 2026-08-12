from app.modules.admin.routes.dashboard import router as dashboard_router
from app.modules.admin.routes.payment_cards import (
    router as payment_cards_router,
)
from app.modules.admin.routes.payments import (
    router as payments_router,
)

__all__ = (
    "dashboard_router",
    "payment_cards_router",
    "payments_router",
)
