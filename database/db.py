import asyncpg

DB_DSN = "postgresql://localhost/postgres"

async def get_connection():
    print("🔌 Подключаемся к базе данных...")
    conn = await asyncpg.connect(dsn=DB_DSN)
    print("✅ БД подключена!")
    return conn