from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


def get_home_keyboard() -> InlineKeyboardMarkup:
    """
    NovaHub bosh sahifasi uchun inline keyboard.
    """

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🌐 Web Panel",
                    callback_data="home:web_panel",
                ),
                InlineKeyboardButton(
                    text="📢 Rasmiy kanal",
                    callback_data="home:channel",
                ),
            ],
        ],
    )
