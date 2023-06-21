from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config_bot.config import bot_api_token

# объявления переменных бота и диспетчера
bot = Bot(token=bot_api_token)
dp = Dispatcher(bot, storage=MemoryStorage())
