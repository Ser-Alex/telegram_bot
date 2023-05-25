import os
from dotenv import load_dotenv, find_dotenv


# проверка окружения на отсутствие файла .env
if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()


# переменные загруженные из файла .env
bot_api_token = os.getenv("BOT_API_TOKEN")
keys_api = [os.getenv('API_KEY_1'), os.getenv('API_KEY_2'), os.getenv('API_KEY_3')]