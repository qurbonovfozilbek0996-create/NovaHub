from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
)


def get_main_menu() -> ReplyKeyboardMarkup:
    """
    NovaHub asosiy menyusi.
    """

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="🌐 Web Panel",
                ),
            ],
            [
                KeyboardButton(
                    text="📢 Rasmiy kanal",
                ),
            ],
        ],
        resize_keyboard=True,
        is_persistent=True,
    )
