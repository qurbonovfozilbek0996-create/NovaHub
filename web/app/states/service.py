from aiogram.fsm.state import State, StatesGroup


class AddServiceState(StatesGroup):
    provider = State()
    platform = State()
    category = State()
    api_service_id = State()
    name = State()
    description = State()
    sale_price = State()
    markup_percent = State()
    sort_order = State()
    confirm = State()


class EditServiceState(StatesGroup):
    name = State()
    description = State()
    sale_price = State()
    markup_percent = State()
    sort_order = State()
