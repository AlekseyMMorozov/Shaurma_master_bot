from datetime import datetime
from aiogram import types, Dispatcher
from bot_create import bot, dp                #импорт экземпляра бота
from bot_keybords import client_kb        #импорт созданной библиотеки для обработки клавиатур
from database import sqlite_db


@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Здравствуйте!\nЯ - телеграм бот Мастер Шаурмы.\n'
                                                'Для получения списка моих команд, напишите мне "/start",\n "/help" '
                                                'или нажмите соответствующую кнопку на клавиатуре\n'
                                                'Как я могу Вам помочь?', reply_markup=client_kb.kb_client)
        await message.delete()
        print(f'{datetime.now()} - command {message.text}')
    except:
        await message.reply('Для работы с ботом, напишите ему личное сообщение:\nhttps://t.me/Shaurma_master_bot')


@dp.message_handler(commands=['время_работы'])
async def send_opening_time(message: types.Message):
    await bot.send_message(message.from_user.id, 'Мы работаем каждый день с 10:00 до 22:00')
    print(f'{datetime.now()} - command {message.text}')


@dp.message_handler(commands=['адрес'])
async def send_address(message: types.Message):
    await bot.send_message(message.from_user.id, 'Наш адрес: ЖК Москвичка, улица Василия Ощепкова, дом 4\n'
                                                'Вход со стороны магазина Магнит')
    print(f'{datetime.now()} - command {message.text}')

@dp.message_handler(commands=['меню'])
async def send_menu(message: types.Message):
    await sqlite_db.get_menu_from_db(message)
    print(f'{datetime.now()} - command Меню')


def register_handler_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(send_opening_time, commands=['время_работы'])
    dp.register_message_handler(send_address, commands=['адрес'])
    dp.register_message_handler(send_menu, commands=['меню'])
