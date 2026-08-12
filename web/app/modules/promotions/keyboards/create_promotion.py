from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup


def wizard_navigation_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ Orqaga",
                    callback_data="promotion:back",
                ),
                InlineKeyboardButton(
                    text="🏠 Bosh menyu",
                    callback_data="promotion:home",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="❌ Bekor qilish",
                    callback_data="promotion:cancel",
                ),
            ],
        ],
    )


def wizard_confirmation_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Tasdiqlash",
                    callback_data="promotion:confirm",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="✏️ Tahrirlash",
                    callback_data="promotion:edit",
                ),
                InlineKeyboardButton(
                    text="❌ Bekor qilish",
                    callback_data="promotion:cancel",
                ),
            ],
        ],
    )
