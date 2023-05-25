from loader import dp
from aiogram import types, dispatcher
from handlers import reg, my_location
from keyboards.reply import keyboard1
from database.data import user_exist


@dp.message_handler(commands=['start', 'hello-world'], state='*')
async def start_command(message: types.Message, state: dispatcher.FSMContext):
    """
    Функция для телеграм бота, начинает работу с любого состояния путём вызова команды /start или /hello-world
    Предназначена для вывода информации о боте, и начала работы с ним

    :param message: предаётся объект типа класс Message
    :param state: передаётся состояние пользователя
    """
    await message.reply('Здравствуй, друг!✋')
    await message.answer('В нашем боте представлена информация о более чем 8000 городах по всему миру. '
                         'Мы собираем, анализируем и сравниваем данные о стоимости жизни, зарплате, популярных '
                         'туристических местах, погоде, достопримечательностях и любой информации, которая будет '
                         'полезна вам для путешествий, изменения вашего места жительства и расширения кругозора. '
                         'В настоящее время доступна информация о ценах на продукты питания, рестораны, кафе, '
                         'транспорт, коммунальные услуги, одежду, расходы на покупку и аренда квартир, а так же '
                         'средние зарплаты.')

    if user_exist(message.from_id):
        await my_location.my_location_command(message=message)
        await message.answer('Изменить местоположение: /reg')
        await message.answer('Наше меню:', reply_markup=keyboard1())
        return

    await reg.registration_command(message=message, state=state)
