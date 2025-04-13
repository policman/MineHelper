from aiogram import Router, types, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from database.db import get_connection
from aiogram.types import ReplyKeyboardRemove

router = Router()

# Шаги для FSM
class ProfileForm(StatesGroup):
    organization = State()
    profession = State()
    location_tag = State()

# Команда запуска формы
@router.message(F.text == "✏️ Редактировать профиль")
async def start_editing(message: types.Message, state: FSMContext):
    await message.answer("🏢 Введите вашу организацию:")
    await state.set_state(ProfileForm.organization)

@router.message(ProfileForm.organization)
async def get_organization(message: types.Message, state: FSMContext):
    await state.update_data(organization=message.text)
    await message.answer("💼 Введите вашу профессию:")
    await state.set_state(ProfileForm.profession)

@router.message(ProfileForm.profession)
async def get_profession(message: types.Message, state: FSMContext):
    await state.update_data(profession=message.text)
    await message.answer("📍 Введите вашу местность (например, Урал, Сибирь и т.д.):")
    await state.set_state(ProfileForm.location_tag)

@router.message(ProfileForm.location_tag)
async def finish_profile(message: types.Message, state: FSMContext):
    await state.update_data(location_tag=message.text)
    data = await state.get_data()

    # Обновление в БД
    conn = await get_connection()
    await conn.execute("""
        UPDATE users SET organization = $1, profession = $2, location_tag = $3
        WHERE telegram_id = $4
    """, data["organization"], data["profession"], data["location_tag"], message.from_user.id)
    await conn.close()

    await message.answer(
        f"✅ Профиль обновлён!\n\n"
        f"🏢 Организация: {data['organization']}\n"
        f"💼 Профессия: {data['profession']}\n"
        f"📍 Местность: {data['location_tag']}",
        reply_markup=ReplyKeyboardRemove()
    )

    await state.clear()
