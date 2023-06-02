from datetime import datetime
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot_create import bot, dp  # импорт экземпляра бота
from bot_keybords import admin_kb  # импорт созданной библиотеки для обработки клавиатур
from database import sqlite_db

ID = None


class FSM_admin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


""" Проверка на адммина группы"""


@dp.message_handler(commands=['mod'], is_chat_admin=True)
async def get_admin_kb(message: types.Message):
    global ID
    ID = message.from_user.id
    print(f'{datetime.now()} - пользователь {message.from_user.id} начал работу в режиме администратора')
    await bot.send_message(message.from_user.id, 'Привет, хозяин! Чем помочь?', reply_markup=admin_kb.kb_admin)
    await message.delete()

@dp.message_handler(commands=['list'])
async def send_help(message: types.Message):
    if message.from_user.id == ID:
        print(f'{datetime.now()} - действие {message.text} пользователь {message.from_user.id}')
        await bot.send_message(message.from_user.id, '"/mod" - переход в режим администратора (вводить в чате группы)\n'
                                                     '"/add" - добавить пункт в меню (для каждого пункта ввести команду\n'
                                                     '"/del" - режим удаления пунктов меню')



""" Добавлене пунктов меню"""


@dp.message_handler(commands=['add'], state=None)
async def add_pos(message: types.Message):
    if message.from_user.id == ID:
        print(f'{datetime.now()} - действие {message.text} пользователь {message.from_user.id}')
        await FSM_admin.photo.set()
        await message.reply('Отправь мне фото нового товара')


@dp.message_handler(state="*", commands='stop')
@dp.message_handler(Text(equals='stop', ignore_case=True), state="*")
async def cancel_setting(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        print(f'{datetime.now()} - действие {message.text} пользователь {message.from_user.id}')
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('Добавление нового товара отменено')
        print(f'{datetime.now()} - Добавление нового товара отменено')


@dp.message_handler(content_types=['photo'], state=FSM_admin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        print(f'{datetime.now()} - действие {message.text} пользователь {message.from_user.id}')
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSM_admin.next()
        await message.reply('Укажи название продукта')


@dp.message_handler(state=FSM_admin.name)
async def set_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        print(f'{datetime.now()} - действие {message.text} пользователь {message.from_user.id}')
        async with state.proxy() as data:
            data['name'] = message.text
        await FSM_admin.next()
        await message.reply('Отправь краткое описание, например, состав продукта')


@dp.message_handler(state=FSM_admin.description)
async def set_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        print(f'{datetime.now()} - действие {message.text} пользователь {message.from_user.id}')
        async with state.proxy() as data:
            data['description'] = message.text
        await FSM_admin.next()
        await message.reply('Укажи стоимость продукта в рублях, например, 185,50')


@dp.message_handler(state=FSM_admin.price)
async def set_price(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        print(f'{datetime.now()} - действие {message.text} пользователь {message.from_user.id}')
        async with state.proxy() as data:
            data['price'] = message.text

        """Сохранение значений из машины состояний в БД"""
        await sqlite_db.add_menu_db(state)

        await state.finish()
        await message.reply('Товар добавлен в меню')
        print(f'{datetime.now()} - Добавлен пункт меню {data["name"]}')


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_menu_pos(callback_query: types.CallbackQuery):
    await sqlite_db.del_menu_db(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} удалена из меню', show_alert=True)


@dp.message_handler(commands='del')
async def del_menu_item(message: types.Message):
    if message.from_user.id == ID:
        print(f'{datetime.now()} - действие {message.text} пользователь {message.from_user.id}')
        read = await sqlite_db.sql_read()
        for ex in read:
            await bot.send_photo(message.from_user.id, ex[0], f'{ex[1]},\nОписание: {ex[2]}.\nСтоимость: {ex[3]} руб.')
            await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup().\
                                   add(InlineKeyboardButton(f'удалить {ex[1]}', callback_data=f'del {ex[1]}')))


def register_handler_admin(dp: Dispatcher):
    dp.register_message_handler(add_pos, commands=['add'], state=None)
    dp.register_message_handler(cancel_setting, state="*", commands='stop')
    dp.register_message_handler(cancel_setting, Text(equals='stop', ignore_case=True), state="*")
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSM_admin.photo)
    dp.register_message_handler(set_name, state=FSM_admin.name)
    dp.register_message_handler(set_description, state=FSM_admin.description)
    dp.register_message_handler(set_price, state=FSM_admin.price)
    dp.register_message_handler(get_admin_kb, commands=['mod'], is_chat_admin=True)
    dp.register_message_handler(send_help, commands=['list'])

