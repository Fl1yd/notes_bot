import logging

import asyncio
import asyncpg

from datetime import datetime, timedelta
from aiogram import executor

from misc import bot, dp, config

import handlers


async def send_reminders():
    while True:
        current_time = datetime.now()
        reminder_time = current_time + timedelta(minutes=10)
        conn = await asyncpg.connect(config.settings.database_url)
 
        reminders = await conn.fetch("""
            SELECT notes.id, notes.text, users.telegram_id
            FROM notes
            JOIN users ON user_id = users.id
            WHERE reminder_time BETWEEN $1 AND $2
        """, current_time, reminder_time)

        for reminder in reminders:
            await bot.send_message(reminder["telegram_id"], f"Напоминание: {reminder['text']}")
            await conn.execute("""DELETE FROM notes WHERE id = $1""", reminder["id"])

        await conn.close()
        await asyncio.sleep(60)


if __name__ == "__main__":
    logging.basicConfig(level="INFO", format="$ %(message)s")

    loop = asyncio.get_event_loop()
    loop.create_task(send_reminders())

    executor.start_polling(dp, skip_updates=True)
