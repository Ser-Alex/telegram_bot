from loader import dp
from aiogram.types import Message
from database.data import user_exist, user_info
from keyboards.reply import keyboard1


@dp.message_handler(commands='my_location', state='*')
@dp.message_handler(text='Моё местоположение', state='*')
async def my_location_command(message: Message) -> None:
    """
    Функция для телеграм бота, начинает работу с любого состояния путём вызова команды /my_location
    или отправив в чат текст 'Моё местоположение'
    Предназначена для вывода местоположения пользователя из базы данных

    :param message: предаётся объект типа класс Message
    """
    if not user_exist(message.from_id):
        await message.reply('Ты не зарегистрирован 😱')
        await message.answer('Команда для регистрации /reg')
        return

    data = user_info(message.from_id)
    await message.reply('Ты сейчас находишься здесь! \nСтрана: {country} \nГород: {city}'.format(
        country=data[0],
        city=data[1]), reply_markup=keyboard1())
