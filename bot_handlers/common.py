from aiogram import types, Dispatcher
import json, string
from datetime import datetime
from bot_create import dp, bot


@dp.message_handler()
async def send_echo(message: types.Message):
    print(f'{datetime.now()} - command {message.text}, от {message.from_user.id}')
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')}\
        .intersection(set(json.load(open('censor_dictionary_json.json')))) != set():
        await message.reply('Ненормативная лексика запрещена!')
        await message.delete()

    elif message.text == 'Привет':
        await message.answer("От души приветствую!")
    elif message.text == 'привет':
        await message.answer("От души приветствую!")
    else:
        await bot.send_message(message.from_user.id, f' команда {message.text} мне не известна')
        await message.delete()


def register_handler_common(dp: Dispatcher):
    dp.register_message_handler(send_echo)
