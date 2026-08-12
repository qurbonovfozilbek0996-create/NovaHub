from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class CreatePromotionSchema:
    target_type: str | None = None
    target_ids: list[int] | None = None

    discount_type: str | None = None
    discount_value: float | None = None

    starts_at: datetime | None = None
    ends_at: datetime | None = None

    banner_type: str | None = None
    banner_file_id: str | None = None

    post_type: str | None = None
    post_text: str | None = None

    channel_id: int | None = None

    reminder_enabled: bool = False
    reminder_minutes: list[int] | None = None
