from aiogram import types
from aiogram.dispatcher import FSMContext

from database import register_user, get_user
from misc import dp


@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    if not user:
        await message.reply("Привет! Отправьте ваше имя")
        return await state.set_state("name")

    return await message.reply(f"Привет, {user['name']}!")


@dp.message_handler(state="name")
async def name_handler(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)

    await message.reply("Теперь отправьте ваш email")
    return await state.set_state("email")


@dp.message_handler(state="email")
async def email_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    name: str = data["name"]

    await register_user(name, message.text, message.from_user.id)

    await message.reply("Вы успешно зарегистрированы!")
    return await state.finish()
