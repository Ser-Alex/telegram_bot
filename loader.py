from aiogram import Bot, Dispatcher
from config_bot.config import bot_api_token
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# объявления переменных бота и диспетчера
bot = Bot(token=bot_api_token)
dp = Dispatcher(bot, storage=MemoryStorage())

