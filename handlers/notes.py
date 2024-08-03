from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from database import add_note, get_notes, get_user
from misc import dp


@dp.message_handler(commands=["addnote"])
async def addnote_cmd(message: types.Message, state: FSMContext):
    await message.reply("Отправьте текст заметки")
    return await state.set_state("addnote_text")


@dp.message_handler(state="addnote_text")
async def addnote_handler(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)

    await message.reply("Теперь отправьте дату и время напоминания в формате ДД.ММ.ГГГГ ЧЧ:ММ")
    return await state.set_state("addnote_time")


@dp.message_handler(state="addnote_time")
async def addnote_time_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    text: str = data["text"]

    try:
        reminder_time = datetime.strptime(message.text, "%d.%m.%Y %H:%M")
    except ValueError:
        return await message.reply(
            "Неверный формат даты и времени. Пожалуйста, используйте формат ДД.ММ.ГГГГ ЧЧ:ММ"
        )

    user = await get_user(message.from_user.id)
    await add_note(user["id"], text, reminder_time)

    await message.reply("Заметка добавлена!")
    return await state.finish()


@dp.message_handler(commands=["notes"])
async def notes_cmd(message: types.Message):
    user = await get_user(message.from_user.id)
    notes = await get_notes(user["id"])

    if not notes:
        return await message.reply(
            "У вас нет заметок"
        )

    notes_list = "\n".join([f"{note['id']}. {note['text']} - {note['reminder_time']}" for note in notes])
    return await message.reply(
        f"Ваши заметки:\n{notes_list}"
    )
