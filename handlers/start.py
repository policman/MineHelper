from aiogram import Router, types
from aiogram.filters import Command
from database.db import get_connection
from database.users import add_user

router = Router()

@router.message(Command("start"))
async def start_handler(message: types.Message):
    user = message.from_user.model_dump()

    conn = await get_connection()
    await add_user(conn, user)

    # Получим те же данные, которые только что записали
    row = await conn.fetchrow("""
        SELECT first_name, last_name, username, organization, profession, location_tag
        FROM users WHERE telegram_id = $1
    """, user["id"])
    await conn.close()

    # Формируем ответ
    text = (
        f"👋 Привет, {row['first_name']}!\n\n"
        f"📛 Фамилия: {row['last_name'] or '—'}\n"
        f"🔹 Username: @{row['username'] or '—'}\n"
        f"🏢 Организация: {row['organization'] or '—'}\n"
        f"💼 Профессия: {row['profession'] or '—'}\n"
        f"📍 Местность: {row['location_tag'] or '—'}\n"
    )

    await message.answer(text)
