from aiogram import F, Router
from aiogram.types import Message

router = Router(name="common.menu")

@router.message(F.text == "🌐 Web Panel")
async def web_panel_handler(message: Message) -> None:
    await message.answer(
        "🌐 Web Panel tez orada ishga tushadi."
    )
