from datetime import datetime

async def add_user(conn, user: dict):
    now = datetime.now().replace(tzinfo=None)  # ГАРАНТИРОВАННО offset-naive

    await conn.execute("""
        INSERT INTO users (
            telegram_id, first_name, last_name, username, is_bot,
            organization, profession, location_tag, registered_at
        )
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
        ON CONFLICT (telegram_id) DO NOTHING;
    """,
    user["id"],
    user["first_name"],
    user.get("last_name"),
    user.get("username"),
    user.get("is_bot"),
    None,
    None,
    None,
    now)  # ← сюда мы передаём гарантированно naive datetime
