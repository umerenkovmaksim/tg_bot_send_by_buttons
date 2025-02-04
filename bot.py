import logging
from aiogram import Bot, Dispatcher

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)