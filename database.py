import asyncpg
from misc import config


async def register_user(name: str, email: str, telegram_id: int):
    conn = await asyncpg.connect(config.settings.database_url)
    await conn.execute("""
        INSERT INTO users (name, email, telegram_id)
        VALUES ($1, $2, $3)
        ON CONFLICT (telegram_id) DO NOTHING
    """, name, email, telegram_id)
    await conn.close()


async def add_note(user_id: int, text: str, reminder_time: str):
    conn = await asyncpg.connect(config.settings.database_url)
    await conn.execute("""
        INSERT INTO notes (user_id, text, reminder_time)
        VALUES ($1, $2, $3)
    """, user_id, text, reminder_time)
    await conn.close()


async def get_notes(user_id: int):
    conn = await asyncpg.connect(config.settings.database_url)
    rows = await conn.fetch("""
        SELECT id, text, reminder_time
        FROM notes
        WHERE user_id = $1
        ORDER BY reminder_time
    """, user_id)
    await conn.close()
    return rows


async def get_user(telegram_id: int):
    conn = await asyncpg.connect(config.settings.database_url)
    row = await conn.fetchrow("""
        SELECT id, name
        FROM users
        WHERE telegram_id = $1
    """, telegram_id)
    await conn.close()
    return row
