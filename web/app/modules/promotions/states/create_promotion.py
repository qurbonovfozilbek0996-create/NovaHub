from aiogram.fsm.state import State
from aiogram.fsm.state import StatesGroup


class CreatePromotionState(StatesGroup):
    target_type = State()
    target_select = State()

    discount_type = State()
    discount_value = State()

    start_datetime = State()
    end_datetime = State()

    banner_type = State()
    banner_upload = State()

    post_type = State()
    post_text = State()

    channel = State()

    reminder_enabled = State()
    reminder_time = State()

    preview = State()

    confirm = State()
