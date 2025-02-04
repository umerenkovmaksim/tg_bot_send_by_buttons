from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

async def admin_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(
        KeyboardButton(text="Отправить сообщение №1"),
        KeyboardButton(text="Отправить сообщение №2"),
    )
    return builder.as_markup(resize_keyboard=True)