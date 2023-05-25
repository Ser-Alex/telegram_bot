from aiogram import types


def keyboard1() -> types.ReplyKeyboardMarkup:
    """
    Функция клавиатуры с кнопками внизу экрана для телеграмм бота

    :return: возвращает объект класса InlineKeyboardMarkup
    """
    kb = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    kb.add(
        types.KeyboardButton(text='Минимальные значения'),
        types.KeyboardButton(text='Максимальные значения'),
        types.KeyboardButton(text='Поиск значений'),
        types.KeyboardButton(text='История'),
        types.KeyboardButton(text='Помощь'),
        types.KeyboardButton(text='Изменить местоположение'),
        types.KeyboardButton(text='Моё местоположение'),
    )

    return kb
