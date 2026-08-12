from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from sqlalchemy.orm import Session

from app.modules.security.services.pin_service import PinService
from app.modules.common.keyboards.home import get_home_keyboard
from app.models.user import User
from app.modules.security.states import PinState

router = Router(name="security.pin")


@router.message(PinState.waiting_for_pin, F.text)
async def create_pin(
    message: Message,
    state: FSMContext,
) -> None:

    pin = message.text.strip()

    if not pin.isdigit() or len(pin) != 6:
        await message.answer(
            "❌ PIN kod faqat 6 ta raqamdan iborat bo'lishi kerak."
        )
        return

    await state.update_data(first_pin=pin)

    await state.set_state(PinState.waiting_for_pin_confirm)

    await message.answer(
        "🔐 PIN kodni qayta kiriting."
    )

@router.message(PinState.waiting_for_pin_confirm, F.text)
async def confirm_pin(
    message: Message,
    state: FSMContext,
    db: Session,
) -> None:

    data = await state.get_data()

    first_pin = data.get("first_pin")

    second_pin = message.text.strip()

    if first_pin != second_pin:
        await state.clear()

        await message.answer(
            "❌ PIN kodlar mos kelmadi.\n\n"
            "PIN yaratishni boshidan boshlang."
        )
        return

    user = db.query(User).filter(
        User.telegram_id == message.from_user.id
    ).first()

    if user is None:
        await state.clear()

        await message.answer(
            "❌ Foydalanuvchi topilmadi."
        )
        return

    user.pin_hash = PinService.hash_pin(first_pin)

    db.commit()

    await state.clear()

    await message.answer(
        "✅ PIN kod muvaffaqiyatli yaratildi."
    )

    await message.answer(
        "🚀 <b>NovaHub Digital</b>\n\n"
        f"Xush kelibsiz, <b>{message.from_user.full_name}</b>!",
        reply_markup=get_home_keyboard(),
    )
