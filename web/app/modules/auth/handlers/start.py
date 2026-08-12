from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    WebAppInfo,
)

from app.core.config.settings import settings
from app.database.session import AsyncSessionLocal
from app.services.registration_service import RegistrationService

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):

    async with AsyncSessionLocal() as session:
        registration = RegistrationService(session)

        await registration.register_telegram_user(
            telegram_id=message.from_user.id,
            full_name=message.from_user.full_name,
            username=message.from_user.username,
            language="uz",
        )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🌐 Web Panel",
                    web_app=WebAppInfo(
                        url=settings.WEB_APP_URL,
                    ),
                ),
            ],
            [
                InlineKeyboardButton(
                    text="📢 Rasmiy kanal",
                    url="https://t.me/oddiylik_o57",
                ),
            ],
        ],
    )

    await message.answer(
        (
            "👋 <b>NovaHub Digital'ga xush kelibsiz!</b>\n\n"
            "NovaHub — Telegram orqali raqamli xizmatlarni tez, "
            "xavfsiz va qulay boshqarish uchun yaratilgan professional platforma.\n\n"
            "✨ Siz bu yerda:\n"
            "• Xizmatlardan foydalanishingiz\n"
            "• Buyurtmalarni kuzatishingiz\n"
            "• Hamyoningizni boshqarishingiz\n"
            "• Hisobingizni nazorat qilishingiz mumkin.\n\n"
            "Quyidagi tugmalardan birini tanlang."
        ),
        reply_markup=keyboard,
    )
