from loader import dp
from aiogram import types


@dp.message_handler(text='Помощь', state='*')
@dp.message_handler(commands='help', state='*')
async def help_command(message: types.Message) -> None:
    """
    Функция для телеграм бота, начинает работу с любого состояния путём вызова команды /help
    или отправив в чат текст 'Помощь'
    Предназначена для вывода информации о командах телеграмм бота

    :param message: предаётся объект типа класс Message
    """
    await message.answer('Меню команд:\n'
                         '/start - Запустить бота\n'
                         '/low - Минимальные цены\n'
                         '/high - Максимальные цены\n'
                         '/custom - Выбрать диапазон цен\n'
                         '/history - История запросов\n'
                         '/my_location - Ваше местоположение\n'
                         '/reg - Изменить местоположение\n')
