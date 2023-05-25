from aiogram import types


def keyboard1() -> types.InlineKeyboardMarkup:
    """
    Функция клавиатуры после сообщения с кнопками для телеграмм бота

    :return: возвращает объект класса InlineKeyboardMarkup
    """
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton(text='Магазины', callback_data='Markets_kb1'),
        types.InlineKeyboardButton(text='Уход за детьми', callback_data='Childcare_kb1'),
        types.InlineKeyboardButton(text='Рестораны', callback_data='Restaurants_kb1'),
        types.InlineKeyboardButton(text='Транспорт', callback_data='Transportation_kb1'),
        types.InlineKeyboardButton(text='Одежда и обувь', callback_data='Clothing And Shoes_kb1'),
        types.InlineKeyboardButton(text='Спорт и отдых', callback_data='Sports And Leisure_kb1'),
        types.InlineKeyboardButton(text='Покупка квартиры', callback_data='Buy Apartment_kb1')
    )
    kb.row_width = 1
    kb.add(
        types.InlineKeyboardButton(text='Коммунальные платежи', callback_data='Utilities Per Month_kb1'),
        types.InlineKeyboardButton(text='Арендная плата в месяц', callback_data='Rent Per Month_kb1'),
        types.InlineKeyboardButton(text='Зарплата и финансирование', callback_data='Salaries And Financing_kb1'),
    )
    return kb
