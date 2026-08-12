from aiogram.fsm.state import State, StatesGroup


class PinState(StatesGroup):
    """
    PIN yaratish va autentifikatsiya holatlari.
    """

    waiting_for_pin = State()
    waiting_for_pin_confirm = State()
    waiting_for_login_pin = State()
