from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select

from app.core.dependencies.services import get_db_session
from app.modules.api_management.models.provider import ProviderType
from app.modules.api_management.services.provider_service import ProviderService
from app.modules.categories.models.category import Category
from app.modules.platforms.models.platform import Platform
from app.modules.services.keyboards.admin_service_keyboard import api_type_keyboard
from app.modules.services.models.service import Service
from app.modules.services.services.service_service import ServiceService
from app.modules.services.services.service_sync_service import ServiceSyncService

router = Router()


class ServiceAdminState(StatesGroup):
    provider = State()
    platform = State()
    category = State()
    edit_name = State()
    edit_description = State()
    edit_price = State()


def menu_keyboard():
    b = InlineKeyboardBuilder()
    b.button(text="🟢 Sotuvda", callback_data="services:selling")
    b.button(text="⚪ Sotuvda emas", callback_data="services:not_selling")
    b.button(text="➕ Xizmat qo‘shish", callback_data="admin:add_service")
    b.button(text="⬅️ Orqaga", callback_data="admin:panel")
    b.adjust(1)
    return b.as_markup()


def detail_keyboard(s: Service):
    b = InlineKeyboardBuilder()
    b.button(
        text="🔴 Sotuvdan olish" if s.is_active else "🟢 Sotuvga chiqarish",
        callback_data=f"service:{'take' if s.is_active else 'sell'}:{s.id}",
    )
    b.button(text="✏️ Nomini tahrirlash", callback_data=f"service:edit_name:{s.id}")
    b.button(text="💰 Narxini tahrirlash", callback_data=f"service:edit_price:{s.id}")
    b.button(text="📝 Tavsifni tahrirlash", callback_data=f"service:edit_description:{s.id}")
    b.button(text="⬅️ Orqaga", callback_data="services:selling" if s.is_active else "services:not_selling")
    b.adjust(1)
    return b.as_markup()


def list_keyboard(services: list[Service], selling: bool):
    b = InlineKeyboardBuilder()
    for s in services:
        b.button(
            text=f"{'🟢' if selling else '⚪'} {s.name} — {s.sale_price}",
            callback_data=f"service:select:{s.id}",
        )
    b.button(
        text="☑️ Hammasini belgilash",
        callback_data=f"service:select_all:{'selling' if selling else 'not_selling'}",
    )
    b.button(text="➕ Xizmat qo‘shish", callback_data="admin:add_service")
    b.button(text="⬅️ Xizmatlar", callback_data="admin:services")
    b.adjust(1)
    return b.as_markup()


async def get_service(service_id: int):
    async for session in get_db_session():
        return await session.get(Service, service_id)


async def update_service(service_id: int, field: str, value):
    async for session in get_db_session():
        return await ServiceService(session).update_service(
            service_id, **{field: value}
        )


def detail_text(s: Service):
    return (
        "🔧 <b>Xizmat</b>\n\n"
        f"🆔 Service ID: <code>{s.service_id}</code>\n"
        f"🔗 API Service ID: <code>{s.api_service_id}</code>\n\n"
        f"🌐 API nomi:\n{s.api_name or '-'}\n\n"
        f"📌 NovaHub nomi:\n{s.name or '-'}\n\n"
        f"💰 API narxi: {s.api_price}\n"
        f"💵 Sotuv narxi: {s.sale_price}\n\n"
        f"📦 Min: {s.min_quantity}\n"
        f"📦 Max: {s.max_quantity}\n\n"
        f"📝 Tavsif:\n{s.description or '-'}\n\n"
        f"Holati: {'🟢 Sotuvda' if s.is_active else '⚪ Sotuvda emas'}"
    )


@router.callback_query(F.data == "admin:services")
async def admin_services(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        "🛠 <b>Xizmatlar boshqaruvi</b>\n\n"
        "Xizmatlarni boshqarish bo‘limi.",
        reply_markup=menu_keyboard(),
    )
    await callback.answer()


@router.callback_query(F.data == "admin:add_service")
async def add_service(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(ServiceAdminState.provider)
    await callback.message.edit_text(
        "🔌 <b>API ni tanlang</b>",
        reply_markup=api_type_keyboard(),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("service_api:"))
async def select_api(callback: CallbackQuery, state: FSMContext):
    value = callback.data.split(":", 1)[1]

    try:
        provider_type = ProviderType(value.upper())
    except ValueError:
        await callback.answer("❌ Noma'lum API turi.", show_alert=True)
        return

    async for session in get_db_session():
        providers = await ProviderService(session).get_all_providers(
            provider_type=provider_type, only_active=True
        )

    if not providers:
        await callback.message.edit_text(
            "❌ Faol Provider topilmadi.",
            reply_markup=api_type_keyboard(),
        )
        return

    b = InlineKeyboardBuilder()
    for p in providers:
        b.button(text=f"🔌 {p.name}", callback_data=f"service_provider:{p.provider_id}")
    b.button(text="⬅️ API tanlash", callback_data="admin:add_service")
    b.adjust(1)

    await state.update_data(provider_id=None)
    await callback.message.edit_text("🔌 <b>Provider ni tanlang</b>", reply_markup=b.as_markup())
    await callback.answer()


@router.callback_query(F.data.startswith("service_provider:"))
async def select_provider(callback: CallbackQuery, state: FSMContext):
    provider_id = int(callback.data.split(":")[1])
    await state.update_data(provider_id=provider_id)

    async for session in get_db_session():
        result = await session.scalars(
            select(Platform)
            .where(Platform.is_active.is_(True))
            .order_by(Platform.sort_order, Platform.name)
        )
        platforms = list(result.all())

    if not platforms:
        await callback.message.edit_text("❌ Faol platformalar mavjud emas.")
        return

    b = InlineKeyboardBuilder()
    for p in platforms:
        b.button(text=f"📱 {p.name}", callback_data=f"service_platform:{p.id}")
    b.button(text="⬅️ Provider", callback_data="admin:add_service")
    b.adjust(1)

    await state.set_state(ServiceAdminState.platform)
    await callback.message.edit_text("📱 <b>Platformani tanlang</b>", reply_markup=b.as_markup())
    await callback.answer()


@router.callback_query(F.data.startswith("service_platform:"))
async def select_platform(callback: CallbackQuery, state: FSMContext):
    platform_id = int(callback.data.split(":")[1])
    data = await state.get_data()
    provider_id = data.get("provider_id")

    if not provider_id:
        await callback.answer("❌ Provider topilmadi.", show_alert=True)
        return

    async for session in get_db_session():
        result = await session.scalars(
            select(Category)
            .where(
                Category.platform_id == platform_id,
                Category.is_active.is_(True),
            )
            .order_by(Category.sort_order, Category.name)
        )
        categories = list(result.all())

    if not categories:
        await callback.message.edit_text("❌ Faol kategoriyalar mavjud emas.")
        return

    await state.update_data(platform_id=platform_id)
    await state.set_state(ServiceAdminState.category)

    b = InlineKeyboardBuilder()
    for c in categories:
        b.button(text=f"📂 {c.name}", callback_data=f"service_category:{c.id}")
    b.button(text="⬅️ Platforma", callback_data=f"service_provider:{provider_id}")
    b.adjust(1)

    await callback.message.edit_text("📂 <b>Kategoriyani tanlang</b>", reply_markup=b.as_markup())
    await callback.answer()


@router.callback_query(F.data.startswith("service_category:"))
async def select_category(callback: CallbackQuery, state: FSMContext):
    category_id = int(callback.data.split(":")[1])
    data = await state.get_data()
    provider_id = data.get("provider_id")
    platform_id = data.get("platform_id")

    if not provider_id or not platform_id:
        await callback.answer("❌ Sessiya ma'lumotlari topilmadi.", show_alert=True)
        return

    await callback.message.edit_text("🔄 <b>API xizmatlari yuklanmoqda...</b>")

    try:
        async for session in get_db_session():
            services = await ServiceSyncService(session).sync_provider_services(
                provider_id, platform_id, category_id
            )
    except Exception:
        await callback.message.edit_text(
            "❌ API xizmatlarini yuklashda xatolik.\n"
            "Provider sozlamalarini tekshiring."
        )
        return

    if not services:
        await callback.message.edit_text("❌ API'dan xizmatlar topilmadi.")
        return

    b = InlineKeyboardBuilder()
    for s in services:
        b.button(
            text=f"🔹 {s.api_name or s.name}",
            callback_data=f"service_api_select:{s.id}",
        )
    b.button(text="⬅️ Kategoriya", callback_data=f"service_platform:{platform_id}")
    b.adjust(1)

    await callback.message.edit_text(
        f"✅ {len(services)} ta xizmat topildi.\n\n🔧 <b>Xizmatni tanlang:</b>",
        reply_markup=b.as_markup(),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("service_api_select:"))
async def api_service_select(callback: CallbackQuery):
    service = await get_service(int(callback.data.split(":")[1]))

    if not service:
        await callback.answer("❌ Xizmat topilmadi.", show_alert=True)
        return

    await callback.message.edit_text(
        detail_text(service),
        reply_markup=detail_keyboard(service),
    )
    await callback.answer()


async def show_services(callback: CallbackQuery, selling: bool):
    async for session in get_db_session():
        result = await session.scalars(
            select(Service)
            .where(Service.is_active.is_(selling))
            .order_by(Service.sort_order, Service.name)
        )
        services = list(result.all())

    title = "🟢 <b>Sotuvdagi xizmatlar</b>" if selling else "⚪ <b>Sotuvda bo‘lmagan xizmatlar</b>"
    await callback.message.edit_text(
        f"{title}\n\nJami: <b>{len(services)}</b> ta xizmat.",
        reply_markup=list_keyboard(services, selling),
    )
    await callback.answer()


@router.callback_query(F.data == "services:selling")
async def selling(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await show_services(callback, True)


@router.callback_query(F.data == "services:not_selling")
async def not_selling(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await show_services(callback, False)


@router.callback_query(F.data.startswith("service:select:"))
async def select_service(callback: CallbackQuery, state: FSMContext):
    service = await get_service(int(callback.data.split(":")[2]))

    if not service:
        await callback.answer("❌ Xizmat topilmadi.", show_alert=True)
        return

    await state.update_data(selected_service_id=service.id)
    await callback.message.edit_text(
        detail_text(service),
        reply_markup=detail_keyboard(service),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("service:sell:"))
async def sell(callback: CallbackQuery):
    service_id = int(callback.data.split(":")[2])
    service = await update_service(service_id, "is_active", True)
    await callback.message.edit_text(detail_text(service), reply_markup=detail_keyboard(service))
    await callback.answer("🟢 Xizmat sotuvga chiqarildi.")


@router.callback_query(F.data.startswith("service:take:"))
async def take(callback: CallbackQuery):
    service_id = int(callback.data.split(":")[2])
    service = await update_service(service_id, "is_active", False)
    await callback.message.edit_text(detail_text(service), reply_markup=detail_keyboard(service))
    await callback.answer("⚪ Xizmat sotuvdan olindi.")


async def edit_start(callback: CallbackQuery, state: FSMContext, field: str, state_value: State, title: str):
    service = await get_service(int(callback.data.split(":")[2]))
    if not service:
        await callback.answer("❌ Xizmat topilmadi.", show_alert=True)
        return

    await state.update_data(edit_service_id=service.id)
    await state.set_state(state_value)
    current = getattr(service, field) or "-"
    await callback.message.edit_text(
        f"{title}\n\nHozirgi qiymat:\n<code>{current}</code>\n\n"
        "Yangi qiymatni yuboring."
    )
    await callback.answer()


@router.callback_query(F.data.startswith("service:edit_name:"))
async def edit_name_start(callback: CallbackQuery, state: FSMContext):
    await edit_start(callback, state, "name", ServiceAdminState.edit_name, "✏️ <b>NovaHub xizmat nomi</b>")


@router.callback_query(F.data.startswith("service:edit_price:"))
async def edit_price_start(callback: CallbackQuery, state: FSMContext):
    await edit_start(callback, state, "sale_price", ServiceAdminState.edit_price, "💰 <b>NovaHub sotuv narxi</b>")


@router.callback_query(F.data.startswith("service:edit_description:"))
async def edit_description_start(callback: CallbackQuery, state: FSMContext):
    await edit_start(callback, state, "description", ServiceAdminState.edit_description, "📝 <b>NovaHub tavsifi</b>")


@router.message(ServiceAdminState.edit_name)
async def edit_name(message: Message, state: FSMContext):
    value = (message.text or "").strip()
    if not value or len(value) > 255:
        await message.answer("❌ Nom noto‘g‘ri.")
        return

    data = await state.get_data()
    await update_service(data["edit_service_id"], "name", value)
    await state.clear()
    await message.answer("✅ NovaHub nomi yangilandi.\nAPI nomi o‘zgarmaydi.")


@router.message(ServiceAdminState.edit_price)
async def edit_price(message: Message, state: FSMContext):
    try:
        value = float((message.text or "").replace(",", "."))
        if value < 0:
            raise ValueError
    except ValueError:
        await message.answer("❌ Narx noto‘g‘ri.")
        return

    data = await state.get_data()
    await update_service(data["edit_service_id"], "sale_price", value)
    await state.clear()
    await message.answer(f"✅ NovaHub sotuv narxi {value} ga o‘zgartirildi.")


@router.message(ServiceAdminState.edit_description)
async def edit_description(message: Message, state: FSMContext):
    value = (message.text or "").strip()

    if len(value) > 4000:
        await message.answer("❌ Tavsif juda uzun.")
        return

    data = await state.get_data()
    await update_service(data["edit_service_id"], "description", value)
    await state.clear()
    await message.answer("✅ NovaHub tavsifi yangilandi.")


@router.callback_query(F.data.startswith("service:select_all:"))
async def select_all(callback: CallbackQuery, state: FSMContext):
    selling = callback.data.split(":")[2] == "selling"

    async for session in get_db_session():
        result = await session.scalars(
            select(Service.id).where(Service.is_active.is_(selling))
        )
        ids = list(result.all())

    if not ids:
        await callback.answer("Xizmatlar mavjud emas.", show_alert=True)
        return

    for service_id in ids:
        await update_service(service_id, "is_active", not selling)

    await callback.message.edit_text(
        f"✅ {len(ids)} ta xizmat {'sotuvdan olindi' if selling else 'sotuvga chiqarildi'}.",
        reply_markup=menu_keyboard(),
    )
    await callback.answer()
