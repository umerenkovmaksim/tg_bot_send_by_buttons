from aiogram.types import InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from config import BUTTON_FOR_MASS_1, BUTTON_FOR_MASS_2, LINK_FOR_MASS_1, LINK_FOR_MASS_2

async def admin_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(
        KeyboardButton(text="Отправить сообщение №1"),
        KeyboardButton(text="Отправить сообщение №2"),
    )
    return builder.as_markup(resize_keyboard=True)

async def mass_keyboard(button_text, button_url):
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text=button_text, url=button_url),
    )
    return builder.as_markup()
