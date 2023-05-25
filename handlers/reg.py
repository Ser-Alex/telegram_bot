from states.state import SelectLocation
from aiogram import types, dispatcher
from database.data import user_exist, update_user_info, new_user
from utils.util import place_list
from loader import dp
from handlers.my_location import my_location_command


@dp.message_handler(text='Изменить местоположение', state='*')
@dp.message_handler(commands='reg', state='*')
async def registration_command(message: types.Message, state: dispatcher.FSMContext) -> None:
    """
    Функция для телеграм бота, начинает работу с любого состояния путём вызова команды /reg
    или отправив в чат текст 'Изменить местоположение'
    Предназначена для регистрации или изменения местоположения пользователя в базе данных

    :param message: предаётся объект типа класс Message
    :param state: передаётся состояние пользователя
    """
    await message.reply('Напиши название страны, в которой ты сейчас '
                        'находишься,с большой буквы, на английском языке:')
    await state.set_state(SelectLocation.choosing_country_name.state)


@dp.message_handler(state=SelectLocation.choosing_country_name.state)
async def process_choosing_country(message: types.Message, state: dispatcher.FSMContext) -> None:
    """
    Функция для телеграм бота, начинает работу с состояния choosing_country_name
    Предназначена для ввода Страны, и проверки Страны в базе данных API на её существование

    :param message: предаётся объект типа класс Message
    :param state: передаётся состояние пользователя
    """
    if message.text not in [i_elem['country_name'] for i_elem in place_list()]:
        await message.reply('Ошибка, в моих записях нет такой страны попробуй ещё раз😉')
        return

    await state.update_data(country_name=message.text)
    await message.answer('Отлично, теперь напиши название города, в котором ты сейчас '
                         'находишься, так же с большой буквы и на английском языке:')
    await state.set_state(SelectLocation.choosing_city_name.state)


@dp.message_handler(state=SelectLocation.choosing_city_name.state)
async def process_choosing_city(message: types.Message, state: dispatcher.FSMContext) -> None:
    """
    Функция для телеграм бота, начинает работу с состояния choosing_city_name
    Предназначена для ввода города, проверки его в базе данных API, и сохранения данных в базе данных

    :param message: предаётся объект типа класс Message
    :param state: передаётся состояние пользователя
    """
    user_data = await state.get_data()
    list_place = [i_elem['city_name'] for i_elem in place_list() if i_elem['country_name'] == user_data['country_name']]
    if message.text not in list_place:
        await message.reply('Извини, но в моих записях нет такого города, попробуй ещё раз😉')
        return

    await state.update_data(city_name=message.text)
    user_data = await state.get_data()
    await state.finish()

    if user_exist(message.from_id):
        update_user_info(message.from_id, user_data['country_name'], user_data['city_name'])
    else:
        new_user(message.from_id, user_data['country_name'], user_data['city_name'])

    await message.answer('Отлично твои данные сохранены!')
    await my_location_command(message=message)
