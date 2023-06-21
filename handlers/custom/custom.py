from aiogram import types, dispatcher

from loader import dp
from utils.util import city_info, set_history, str_info
from database.data import user_exist, user_info
from keyboards import inline, reply
from states.state import CustomSelect


@dp.message_handler(text='Поиск значений', state='*')
@dp.message_handler(commands='custom', state='*')
async def custom_command(message: types.Message, state: dispatcher.FSMContext) -> None:
    """
    Функция для телеграм бота, начинает работу с любого состояния путём вызова команды /custom
    или отправив в чат текст 'Поиск значений'
    Предназначена для выбора категории с помощью клавиатуры

    :param message: предаётся объект типа класс Message
    :param state: передаётся состояние пользователя
    """
    if not user_exist(message.from_id):
        await message.reply('Ты не зарегистрирован 😱\n'
                            'Команда для регистрации /reg')
        return

    await message.reply('Выберите категорию:', reply_markup=inline.keyboard1())
    await state.set_state(CustomSelect.category_selection.state)


@dp.callback_query_handler(dispatcher.filters.Text(endswith='_kb1'), state=CustomSelect.category_selection.state)
async def selection_category(call: types.CallbackQuery, state: dispatcher.FSMContext) -> None:
    """
    Функция для телеграм бота, начинает работу после работы с клавиатурой inline.keyboard1()
    и состояния category_selection
    Предназначена для ввода пользователем минимальной границы поиска

    :param call: предаётся объект типа класс CallbackQuery
    :param state: передаётся состояние пользователя
    """
    await state.update_data(category=call.data[:-4])
    await call.message.edit_text('Теперь введите минимальную границу диапазона:')
    await state.set_state(CustomSelect.diapason_low_selection.state)


@dp.message_handler(state=CustomSelect.diapason_low_selection.state)
async def selection_diapason_low(message: types.Message, state: dispatcher.FSMContext) -> None:
    """
    Функция для телеграм бота, начинает работу с состояния diapason_low_selection
    Предназначена для проверки корректности ввода пользователем минимальной границы поиска и
    для ввода пользователем максимальной границы поиска

    :param message: предаётся объект типа класс Message
    :param state: передаётся состояние пользователя
    """
    try:
        message.text = float(message.text)
        if message.text < 0:
            raise ValueError
    except ValueError:
        await message.reply('Ошибка ввода, попробуй ещё раз😉')
        return

    await state.update_data(min=message.text)
    await message.answer('Супер, теперь введи максимальную границу диапазона:')
    await state.set_state(CustomSelect.diapason_high_selection.state)


@dp.message_handler(state=CustomSelect.diapason_high_selection.state)
async def selection_diapason_high(message: types.Message, state: dispatcher.FSMContext) -> None:
    """
    Функция для телеграм бота, начинает работу с состояния diapason_high_selection
    Предназначена для проверки корректности ввода пользователем максимальной границы поиска и
    для ввода числа, которое будет использоваться дальше

    :param message: предаётся объект типа класс Message
    :param state: передаётся состояние пользователя
    """
    try:
        message.text = float(message.text)
        user_data = await state.get_data()
        if message.text < user_data['min']:
            raise ValueError
    except ValueError:
        await message.reply('Ошибка ввода, попробуй ещё раз😉')
        return

    await state.update_data(max=message.text)
    await message.answer('Отлично, теперь введи число, это будет количество предложений, которые мы отправим тебе:')
    await state.set_state(CustomSelect.quantity_selection.state)


@dp.message_handler(state=CustomSelect.quantity_selection.state)
async def selection_quantity(message: types.Message, state: dispatcher.FSMContext) -> None:
    """
    Функция для телеграм бота, начинает работу с состояния quantity_selection
    Предназначена для проверки корректности ввода пользователем числа, которое используется для вывода информации и
    вывода информации по заданным критериям с учетом местонахождения пользователя, а так же для сохранения истории

    :param message: предаётся объект типа класс Message
    :param state: передаётся состояние пользователя
    """
    try:
        message.text = int(message.text)
    except ValueError:
        await message.reply('Ошибка ввода, попробуй ещё раз😉')
        return

    data = user_info(message.from_id)
    country = data[0]
    city = data[1]
    res = city_info(country, city)['prices']
    user_data = await state.get_data()
    await state.finish()

    elements = [i_elem for i_elem in res if i_elem['category_name'] == user_data['category']]
    user_diapason = set(range(int(user_data['min']), int(user_data['max'])))
    elements = [i_elem for i_elem in elements if set(range(int(i_elem['min']), int(i_elem['max']))) & user_diapason]

    if not len(elements):
        await message.answer('В таком диапазоне нет, предложений')
        return

    if len(elements) < int(message.text):
        await message.answer(f'Такого количества нет, выведено - {len(elements)}')
        for i_elem in elements:
            await message.answer(str_info(i_elem))

        history = f"{country} {city} custom {user_data['category'].replace(' ', '')} {len(elements)} " \
                  f"{user_data['min']} {user_data['max']}"

        set_history(message.from_id, history)
        await message.answer(text='Меню:', reply_markup=reply.keyboard1())
        return

    for i_num in range(int(message.text)):
        i_elem = elements[i_num]
        await message.answer(str_info(i_elem))

    history = f"{country} {city} custom {user_data['category'].replace(' ', '')} {message.text} " \
              f"{user_data['min']} {user_data['max']}"

    set_history(message.from_id, history)
    await message.answer(text='Меню:', reply_markup=reply.keyboard1())
