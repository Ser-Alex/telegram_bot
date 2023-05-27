import sqlite3
from main import logging
from config_bot.config import path_data
import os.path


def start_data() -> None:
    """
    Функция проверки существования базы данных, и создания её, если таковой не имеется
    """
    if os.path.exists(path_data):
        return

    try:
        sqlite_connection = sqlite3.connect(path_data)
        sqlite_create_table_user_location = '''CREATE TABLE  user_location(
                                    id INTEGER ,
                                    country TEXT NOT NULL,
                                    city TEXT NOT NULL );'''

        sqlite_create_table_user_history = '''CREATE TABLE  user_history(
                                    id INTEGER ,
                                    history TEXT NOT NULL);'''

        cursor = sqlite_connection.cursor()
        cursor.execute(sqlite_create_table_user_location)

        cursor = sqlite_connection.cursor()
        cursor.execute(sqlite_create_table_user_history)

        sqlite_connection.commit()
        cursor.close()
        sqlite_connection.close()

    except sqlite3.Error:
        logging.error('sqlite3.Error', exc_info=True)


def user_exist(user_id: int) -> bool:
    """
    Функция проверки существования пользователя в базе данных, проверка по user_id

    :param user_id: передаётся id пользователя
    :return: bool
    """
    start_data()
    try:
        sqlite_connection = sqlite3.connect(path_data)
        cursor = sqlite_connection.cursor()

        sql_select = """select * from user_location where id = ?"""
        cursor.execute(sql_select, (user_id,))
        rec = cursor.fetchall()

        sqlite_connection.commit()
        cursor.close()
        sqlite_connection.close()
        if rec:
            return True
        return False

    except sqlite3.Error:
        logging.error('sqlite3.Error', exc_info=True)


def user_info(user_id: int) -> tuple[str, str] or False:
    """
    Функция для получения данных(Страна и город) пользователя из базы данных

    :param user_id: передаётся id пользователя
    :return: кортеж(Страна, город) или False
    """
    start_data()
    try:
        sqlite_connection = sqlite3.connect(path_data)
        cursor = sqlite_connection.cursor()
        sql_select = """select * from user_location where id = ?"""
        cursor.execute(sql_select, (user_id,))
        rec = cursor.fetchall()

        sqlite_connection.commit()
        cursor.close()
        sqlite_connection.close()
        return rec[0][1], rec[0][2]

    except sqlite3.Error:
        logging.error('sqlite3.Error', exc_info=True)


def new_user(user_id: int, country: str, city: str) -> None:
    """
    Функция для регистрации нового пользователя в базе данных

    :param user_id: передаётся id пользователя
    :param country: передаётся название страны
    :param city: передаётся название города
    """
    start_data()
    try:
        sqlite_connection = sqlite3.connect(path_data)
        cursor = sqlite_connection.cursor()
        sql_insert = """INSERT INTO user_location
                          (id, country, city)
                          VALUES
                          (?, ?, ?);"""
        cursor.execute(sql_insert, (user_id, country, city,))

        sqlite_connection.commit()
        cursor.close()
        sqlite_connection.close()

    except sqlite3.Error:
        logging.error('sqlite3.Error', exc_info=True)


def update_user_info(user_id: int, country: str, city: str) -> None:
    """
    Функция для обновления информации о пользователе в базе данных

    :param user_id: передаётся id пользователя
    :param country: передаётся название страны
    :param city: передаётся название города
    """
    start_data()
    try:
        sqlite_connection = sqlite3.connect(path_data)
        cursor = sqlite_connection.cursor()
        sql_update = """Update user_location set country = ?, city = ? where id = ?"""
        cursor.execute(sql_update, (country, city, user_id,))

        sqlite_connection.commit()
        cursor.close()
        sqlite_connection.close()
    except sqlite3.Error:
        logging.error('sqlite3.Error', exc_info=True)


def check_history(user_id: int) -> bool:
    """
    Функция для проверки наличия истории у пользователя

    :param user_id: передаётся id пользователя
    :return: bool
    """
    start_data()
    try:
        sqlite_connection = sqlite3.connect(path_data)
        cursor = sqlite_connection.cursor()
        sql_select = """select * from user_history where id = ?"""
        cursor.execute(sql_select, (user_id,))
        rec = cursor.fetchall()

        sqlite_connection.commit()
        cursor.close()
        sqlite_connection.close()

        if rec:
            return True
        return False

    except sqlite3.Error:
        logging.error('sqlite3.Error', exc_info=True)


def new_history(user_id: int, str_history: str) -> None:
    """
    Функция для добавление истории пользователя в базу данных

    :param user_id: передаётся id пользователя
    :param str_history: передаётся история
    """
    start_data()
    try:
        sqlite_connection = sqlite3.connect(path_data)
        cursor = sqlite_connection.cursor()
        sql_insert = """INSERT INTO user_history
                                  (id, history)
                                  VALUES
                                  (?, ?);"""
        cursor.execute(sql_insert, (user_id, str_history + '*',))
        sqlite_connection.commit()
        cursor.close()
        sqlite_connection.close()

    except sqlite3.Error:
        logging.error('sqlite3.Error', exc_info=True)


def update_history(user_id: int, str_history: str) -> None:
    """
    Функция для добавления истории запросов, хранится не больше 10 запросов

    :param user_id: передаётся id пользователя
    :param str_history: передаётся история
    """
    start_data()
    try:
        sqlite_connection = sqlite3.connect(path_data)
        cursor = sqlite_connection.cursor()
        sql_select = """select * from user_history where id = ?"""
        cursor.execute(sql_select, (user_id,))
        rec = cursor.fetchall()[0][1]
        if rec.count('*') == 10:
            rec_list = rec.split('*')[:-2]
            rec = '*'.join(rec_list) + '*'

        sqlite_connection.commit()
        sql_update = """Update user_history set history = ? where id = ?"""
        cursor.execute(sql_update, (str_history + '*' + rec, user_id,))

        sqlite_connection.commit()
        cursor.close()
        sqlite_connection.close()
    except sqlite3.Error:
        logging.error('sqlite3.Error', exc_info=True)


def get_history_list(user_id: int) -> str:
    """
    Функция для получения истории пользователя из базы

    :param user_id: передаётся id пользователя
    :return: строку историй запросов
    """
    start_data()
    try:
        sqlite_connection = sqlite3.connect(path_data)
        cursor = sqlite_connection.cursor()
        sql_select = """select * from user_history where id = ?"""
        cursor.execute(sql_select, (user_id,))
        rec = cursor.fetchall()[0][1]

        sqlite_connection.commit()
        cursor.close()
        sqlite_connection.close()
        return rec.split('*')[:-1]

    except sqlite3.Error:
        logging.error('sqlite3.Error', exc_info=True)
