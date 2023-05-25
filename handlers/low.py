from loader import dp
from aiogram import types, dispatcher
from utils.util import city_info, set_history, str_info
from database.data import user_exist, user_info
from keyboards import inline, reply
from states.state import LowSelect


@dp.message_handler(text='Минимальные значения', state='*')
@dp.message_handler(commands='low', state='*')
async def low_command(message: types.Message, state: dispatcher.FSMContext) -> None:
    """
    Функция для телеграм бота, начинает работу с любого состояния путём вызова команды /low
    или отправив в чат текст 'Минимальные значения'
    Предназначена для выбора категории с помощью клавиатуры

    :param message: предаётся объект типа класс Message
    :param state: передаётся состояние пользователя
    """
    if not user_exist(message.from_id):
        await message.reply('Ты не зарегистрирован 😱\n'
                            'Команда для регистрации /reg')
        return

    await message.reply('Выберите категорию:', reply_markup=inline.keyboard1())
    await state.set_state(LowSelect.category_selection.state)


@dp.callback_query_handler(dispatcher.filters.Text(endswith='_kb1'), state=LowSelect.category_selection.state)
async def selection_category(call: types.CallbackQuery, state: dispatcher.FSMContext) -> None:
    """
    Функция для телеграм бота, начинает работу после работы с клавиатурой inline.keyboard1()
    и состояния category_selection
    Предназначена для ввода числа, которое будет использоваться дальше

    :param call: предаётся объект типа класс CallbackQuery
    :param state: передаётся состояние пользователя
    """
    await state.update_data(category=call.data[:-4])
    await call.message.edit_text('Отлично, теперь введи число, это будет количество '
                                 'предложений, которые мы отправим тебе:')
    await state.set_state(LowSelect.quantity_selection.state)


@dp.message_handler(state=LowSelect.quantity_selection.state)
async def selection_quantity(message: types.Message, state: dispatcher.FSMContext) -> None:
    """
    Функция для телеграм бота, начинает работу с состояния quantity_selection
    Предназначена для проверки корректности ввода пользователем числа, которое используется для вывода информации и
    вывода информации с учетом местонахождения пользователя, а так же для сохранения истории

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

    elements = sorted(elements, key=lambda x: x['min'])
    if len(elements) < message.text:
        await message.answer(f'Такого количества нет, выведено - {len(elements)}')
        for i_elem in elements:
            await message.answer(str_info(i_elem))

        history = f"{country} {city} low {user_data['category'].replace(' ', '')} {len(elements)}"
        set_history(message.from_id, history)

        await message.answer(text='Меню:', reply_markup=reply.keyboard1())
        return

    for i_num in range(int(message.text)):
        i_elem = elements[i_num]
        await message.answer(str_info(i_elem))

    history = f"{country} {city} low {user_data['category'].replace(' ', '')} {message.text}"
    set_history(message.from_id, history)
    await message.answer(text='Меню:', reply_markup=reply.keyboard1())
