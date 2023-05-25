from aiogram.dispatcher.filters.state import State, StatesGroup


class SelectLocation(StatesGroup):
    """
    Дочерний класс SelectLocation от класса StatesGroup
    имеет два состояния для регистрации пользователя в базе данных(страна, город)
    """
    choosing_country_name = State()
    choosing_city_name = State()


class LowSelect(StatesGroup):
    """
    Дочерний класс LowSelect от класса StatesGroup
    имеет два состояния для запроса пользователя в категории Минимальные цены
    """
    category_selection = State()
    quantity_selection = State()


class HighSelect(StatesGroup):
    """
    Дочерний класс HighSelect от класса StatesGroup
    имеет два состояния для запроса пользователя в категории Максимальные цены
    """
    category_selection = State()
    quantity_selection = State()


class CustomSelect(StatesGroup):
    """
    Дочерний класс CustomSelect от класса StatesGroup
    имеет четыре состояния для запроса пользователя в диапазоне цен введённых пользователем
    """
    category_selection = State()
    diapason_low_selection = State()
    diapason_high_selection = State()
    quantity_selection = State()
