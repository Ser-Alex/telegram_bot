from loader import dp
from aiogram import types


@dp.message_handler()
async def echo(message: types.Message) -> None:
    """
    Функция для телеграм бота, начинает работу если сообщение нигде не обрабатывается,
    то есть сообщение, которое не ожидается ботом

    :param message: предаётся объект типа класс Message
    """
    await message.reply('Я вас не понимаю 😓 \nВоспользуйтесь командой /help')
