from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def api_type_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="📈 SMM API",
        callback_data="service_api:smm",
    )

    builder.button(
        text="⭐ Telegram API",
        callback_data="service_api:telegram",
    )

    builder.button(
        text="📱 Numbers API",
        callback_data="service_api:numbers",
    )

    builder.button(
        text="⬅️ Orqaga",
        callback_data="admin:services",
    )

    builder.adjust(1)

    return builder.as_markup()
