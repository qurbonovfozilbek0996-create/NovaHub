from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.orm import Session

from app.common.menus import get_main_menu
from app.modules.auth.keyboards import phone_keyboard
from app.modules.auth.states import RegistrationState
from app.modules.security.states import PinState
from app.services.user_service import UserService

router = Router(name="auth.start")


@router.message(CommandStart())
async def start_handler(
    message: Message,
    state: FSMContext,
    db: Session,
) -> None:

    user_service = UserService(db)

    user = user_service.get_by_telegram_id(message.from_user.id)

    # Yangi foydalanuvchi
    if user is None:
        await state.set_state(RegistrationState.waiting_for_phone)

        await message.answer(
            "👋 Assalomu alaykum!\n\n"
            "NovaHub Digital platformasiga xush kelibsiz.\n\n"
            "Ro'yxatdan o'tishni boshlash uchun telefon raqamingizni yuboring.",
            reply_markup=phone_keyboard(),
        )
        return

    # PIN hali yaratilmagan
    if not user.pin_hash:
        await state.set_state(PinState.waiting_for_pin)

        await message.answer(
            "🔐 Akkauntingiz xavfsizligi uchun 4 xonali PIN kod yarating."
        )
        return

    # PIN mavjud
    await state.set_state(PinState.waiting_for_login_pin)

    await message.answer(
        "👋 Qaytganingizdan xursandmiz!\n\n"
        "NovaHub Digital hisobingizga kirishni davom ettirish uchun "
        "o'zingiz yaratgan 4 xonali PIN kodni kiriting."
    )
