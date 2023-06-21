from aiogram import executor

from loader import dp
import logging
import handlers


# подключаем логирование
logging = logging
logging.basicConfig(
    level=logging.DEBUG,
    filename='log.log',
    filemode='w',
    format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
    datefmt='%H:%M:%S',
    )

# запускаем бота
if __name__ == '__main__':
    executor.start_polling(dp)
