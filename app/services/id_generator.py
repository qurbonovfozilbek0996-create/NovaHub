from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.wallet import Wallet


def generate_wallet_id(db: Session) -> str:
    last_wallet = db.query(func.max(Wallet.id)).scalar() or 0
    next_id = last_wallet + 1
    return f"WL{next_id:06d}"
