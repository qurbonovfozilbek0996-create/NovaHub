from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.orm import Session

from app.models.user import User
from app.modules.security.services.pin_service import PinService
from app.modules.security.states import PinState
from app.modules.common.keyboards.home import get_home_keyboard

router = Router(name="security.create_pin")


@router.message(PinState.waiting_for_pin)
async def create_pin_step_1(
    message: Message,
    state: FSMContext,
) -> None:
    pin = message.text.strip()

    if not pin.isdigit() or len(pin) != 4:
        await message.answer(
            "❌ PIN faqat 4 xonali raqamdan iborat bo'lishi kerak."
        )
        return

    await state.update_data(pin=pin)
    await state.set_state(PinState.waiting_for_pin_confirm)

    await message.answer(
        "🔐 PIN kodni qayta kiriting."
    )


@router.message(PinState.waiting_for_pin_confirm)
async def create_pin_step_2(
    message: Message,
    state: FSMContext,
    db: Session,
) -> None:
    confirm_pin = message.text.strip()

    data = await state.get_data()
    pin = data["pin"]

    if pin != confirm_pin:
        await state.set_state(PinState.waiting_for_pin)

        await message.answer(
            "❌ PIN kodlar mos kelmadi.\n\nQaytadan kiriting."
        )
        return

    user = (
        db.query(User)
        .filter(User.telegram_id == message.from_user.id)
        .first()
    )

    PinService(db).create_pin(user, pin)

    await state.clear()

    await message.answer(
        "✅ PIN muvaffaqiyatli yaratildi.\n\n"
        "NovaHub'ga xush kelibsiz!",
        reply_markup=get_home_keyboard(),
    )
