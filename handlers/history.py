from loader import dp
from aiogram import types
from database.data import get_history_list
from utils.util import category_dict
from keyboards import reply


@dp.message_handler(text='История', state='*')
@dp.message_handler(commands='history', state='*')
async def history_command(message: types.Message) -> None:
    """
    Функция для телеграм бота, начинает работу с любого состояния путём вызова команды /history
    или отправив в чат текст 'История'
    Предназначена для вывода истории пользователя из базы данных

    :param message: предаётся объект типа класс Message
    """
    await message.answer('Последние запросы:')
    try:
        for i_history in get_history_list(message.from_id):
            history = i_history.split()

            if history[4] == 'low':
                str_history = f'Дата-время: {history[0]} {history[1]} \n' \
                              f'Местоположение: {history[2]} {history[3]} \n' \
                              f'Минимальные цены: \n' \
                              f'Категория: {category_dict[history[5]]} \n' \
                              f'Выведено: {history[6]}'
                await message.answer(str_history)

            elif history[4] == 'high':
                str_history = f'Дата-время: {history[0]} {history[1]} \n' \
                              f'Местоположение: {history[2]} {history[3]} \n' \
                              f'Максимальные цены: \n' \
                              f'Категория: {category_dict[history[5]]} \n' \
                              f'Выведено: {history[6]}'
                await message.answer(str_history)

            elif history[4] == 'custom':
                str_history = f'Дата-время: {history[0]} {history[1]} \n' \
                              f'Местоположение: {history[2]} {history[3]} \n' \
                              f'Цены: от {history[7]} до {history[8]}\n' \
                              f'Категория: {category_dict[history[5]]} \n' \
                              f'Выведено: {history[6]}'
                await message.answer(str_history)

        await message.answer(text='Меню:', reply_markup=reply.keyboard1())
    except IndexError:
        await message.answer('Ты ещё не делал запросы')
        await message.answer(text='Меню:', reply_markup=reply.keyboard1())
