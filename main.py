import asyncio

from aiogram import Router, types, filters, F

from bot import bot, dp
from config import *
from database import *
from keyboards import admin_keyboard, mass_keyboard

asyncio.get_event_loop().run_until_complete(init_db())

@dp.message(filters.CommandStart())
async def start(message: types.Message):
    await message.answer(HELLO_MESSAGE)
    await asyncio.sleep(2)
    await message.answer(MESSAGE_AFTER_DELAY)
    await add_user(message.from_user.id)

    if message.from_user.id in ADMIN_IDS:
        await message.answer("Админ-панель:", reply_markup=await admin_keyboard())
        
@dp.message(F.text.startswith("Отправить сообщение"))
async def mass_send_handler(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return

    message_type = message.text[-1]
    users = await get_users_for_m1() if message_type == "1" else await get_users_for_m2()
    message_text = MESSAGE_FOR_MASS_1 if message_type == "1" else MESSAGE_FOR_MASS_2
    button_text = BUTTON_FOR_MASS_1 if message_type == "1" else BUTTON_FOR_MASS_2
    button_url = LINK_FOR_MASS_1 if message_type == "1" else LINK_FOR_MASS_2

    success = 0
    failed = 0

    for user in users:
        if int(user['telegram_id']) in ADMIN_IDS:
            continue
        try:
            await bot.send_message(user['telegram_id'], message_text, reply_markup=await mass_keyboard(button_text, button_url))
            await mark_message_sent(user['telegram_id'], message_type)
            success += 1
        except Exception:
            failed += 1
        await asyncio.sleep(0.1)

    await message.answer(
        f"Рассылка {message_type} завершена\n"
        f"Успешно: {success}\n"
        f"Не удалось: {failed}"
    )
    
async def main():
    await dp.start_polling(bot)
    

if __name__ == '__main__':
    asyncio.run(main())