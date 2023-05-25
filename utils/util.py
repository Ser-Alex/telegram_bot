import datetime
import requests
from database.data import new_history, update_history, check_history
from config_bot.config import keys_api
from main import logging


# Словарь для хранения категорий(чтобы inline клавиатура не на Английском была, а на русском)
category_dict = {'Markets': 'Магазины', 'Childcare': 'Уход за детьми', 'Restaurants': 'Рестораны',
                 'Transportation': 'Транспорт', 'ClothingAndShoes': 'Одежда и обувь',
                 'SportsAndLeisure': 'Спорт и отдых', 'BuyApartment': 'Покупка квартиры',
                 'UtilitiesPerMonth': 'Коммунальные платежи', 'RentPerMonth': 'Арендная плата в месяц',
                 'SalariesAndFinancing': 'Зарплата и финансирование'}


def place_list() -> dict:
    """
    Функция для запроса от API, информации разных стран и городов мира
    использует список ключей для обхода ограничений API

    :return: словарь с городами и странами
    """
    url = "https://cost-of-living-and-prices.p.rapidapi.com/cities"
    for i_key in keys_api:
        headers = {
            "X-RapidAPI-Key": i_key,
            "X-RapidAPI-Host": "cost-of-living-and-prices.p.rapidapi.com"
        }
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            return res.json()['cities']

    logging.error('Функция не получила код 200 от сервера API!')


def city_info(country_name: str, city_name: str) -> dict:
    """
    Функция для запроса от API, информации о ценах в стране и городе введённых пользователем
    использует список ключей для обхода ограничений API

    :param country_name: передаётся название страны,
    :param city_name: передаётся название города,
    :return: словарь с ценами по разным категориям
    """
    url = "https://cost-of-living-and-prices.p.rapidapi.com/prices"
    querystring = {"city_name": city_name, "country_name": country_name}
    for i_key in keys_api:
        headers = {
            "X-RapidAPI-Key": i_key,
            "X-RapidAPI-Host": "cost-of-living-and-prices.p.rapidapi.com"
        }
        res = requests.get(url, headers=headers, params=querystring, timeout=10)
        if res.status_code == 200:
            return res.json()

    logging.error('Функция не получила код 200 от сервера API!')


def set_history(user_id: int, str_history: str) -> None:
    """
    Функция для сохранения истории в зависимости от того была ли она у пользователя раннее или нет
    добавляет в историю текущее время

    :param user_id: передаётся id пользователя,
    :param str_history: передаётся строка истории
    """
    data_time = str(datetime.datetime.now())[:-7]
    str_history = f'{data_time} {str_history}'
    if check_history(user_id):
        update_history(user_id, str_history)
    else:
        new_history(user_id, str_history)


def str_info(element: dict) -> str:
    """
    Функция для оформления словаря от API в информативную строку

    :param element: передаётся словарь
    :return: str
    """
    text_info = 'Название: {name} \nКатегория: {category} \nМинимальная цена: {min}\n Средняя цена: {avg} ' \
                '\nМаксимальная цена: {max}\nМера: {measure}'.format(
                            name=element['item_name'], category=element['category_name'], min=element['min'],
                            avg=element['avg'], max=element['max'], measure=element['measure'])

    if 'currency_code' in element.keys():
        text_info += f'\nВалюта: {element["currency_code"]}'

    return text_info
