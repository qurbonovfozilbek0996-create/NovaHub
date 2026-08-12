from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import Session

from app.modules.auth.states import RegistrationState
from app.services.registration_service import RegistrationService

from app.modules.security.states import PinState

router = Router(name="auth.register")

@router.message(RegistrationState.waiting_for_phone, F.contact)
async def register_handler(
    message: Message,
    state: FSMContext,
    db: Session,
) -> None:
    if message.contact.user_id != message.from_user.id:
        await message.answer(
            "❌ Iltimos, o'zingizning telefon raqamingizni yuboring."
        )
        return

    registration_service = RegistrationService(db)

    registration_service.register_user(
        telegram_id=message.from_user.id,
        full_name=message.from_user.full_name,
        username=message.from_user.username,
        phone_number=message.contact.phone_number,
    )

    await state.set_state(PinState.waiting_for_pin)

    await message.answer(
        "🎉 Tabriklaymiz!\n\n"
        "Siz NovaHub'dan muvaffaqiyatli ro'yxatdan o'tdingiz.\n\n"
        "🔐 Endi akkauntingiz xavfsizligi uchun 4 xonali PIN kod yarating."
    )
