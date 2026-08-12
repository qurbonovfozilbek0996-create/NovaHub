from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.orm import Session

from app.common.menus import get_main_menu
from app.modules.security.services.pin_service import PinService
from app.modules.security.states import PinState
from app.repositories.user_repository import UserRepository

router = Router(name="security.login_pin")


@router.message(PinState.waiting_for_login_pin)
async def login_pin_handler(
    message: Message,
    state: FSMContext,
    db: Session,
) -> None:

    pin = message.text.strip()

    if not pin.isdigit() or len(pin) != 4:
        await message.answer(
            "❌ PIN kod 4 ta raqamdan iborat bo'lishi kerak."
        )
        return

    user = UserRepository(db).get_by_telegram_id(
        message.from_user.id
    )

    if not user:
        await state.clear()

        await message.answer(
            "❌ Foydalanuvchi topilmadi."
        )
        return

    service = PinService(db)

    if service.is_blocked(user):
        await message.answer(
            "🔒 Juda ko'p noto'g'ri urinish.\n\n"
            "15 daqiqadan so'ng qayta urinib ko'ring."
        )
        return

    if not service.verify(user, pin):
        qolgan = service.MAX_ATTEMPTS - user.pin_attempts

        await message.answer(
            f"❌ PIN kod noto'g'ri.\n"
            f"Qolgan urinishlar: {qolgan}"
        )
        return

    await state.clear()

    builder = InlineKeyboardBuilder()

    builder.button(
        text="🌐 Web Panel",
        url="https://web.novahub.uz"
    )

    builder.button(
        text="📢 Rasmiy kanal",
        url="https://t.me/NovaHubOfficial"
    )

    builder.adjust(2)

    await message.answer(
        "🎉 <b>NovaHub Digital ✨ ga xush kelibsiz!</b>\n\n"
        "NovaHub — Telegram uchun zamonaviy raqamli xizmatlar platformasi.\n\n"
        "Platformamiz orqali siz:\n\n"
        "⭐ Telegram Stars xarid qilishingiz\n"
        "💎 Telegram Premium faollashtirishingiz\n"
        "🎁 Telegram Gifts yuborishingiz\n"
        "📱 Virtual raqamlar xarid qilishingiz\n"
        "👛 NovaHub Wallet orqali to'lovlarni boshqarishingiz\n"
        "📦 Buyurtmalaringizni real vaqt rejimida kuzatishingiz mumkin.\n\n"
        "🔒 Hisobingiz zamonaviy xavfsizlik tizimi bilan himoyalangan va barcha ma'lumotlaringiz ishonchli saqlanadi.\n\n"
        "🚀 Boshlash uchun quyidagi tugmalar yoki menyudan foydalaning.",
        parse_mode="HTML",
        reply_markup=builder.as_markup(),
    )

    await message.answer(
        "🏠 Asosiy menyu",
        reply_markup=get_main_menu(),
    )
