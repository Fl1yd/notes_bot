import asyncpg
import asyncio

database_config = {
    "host": "localhost",
    "port": 5432,
    "user": "testoviy_user",
    "password": "givemeyourpassword",
    "database": "testovoe_zadanie"
}


async def create_tables():
    conn = await asyncpg.connect(
        user="testoviy_user",
        password="givemeyourpassword",
        database="testovoe_zadanie",
        host="localhost",
        port=5432
    )

    try:
        await conn.execute(
            """CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                telegram_id INTEGER UNIQUE NOT NULL
            );

            CREATE TABLE IF NOT EXISTS notes (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                text TEXT NOT NULL,
                reminder_time TIMESTAMP NOT NULL
            );"""
        )
        print("Таблица создана успешно")
    finally:
        await conn.close()


if __name__ == "__main__":
    asyncio.run(create_tables())
