from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b0 = KeyboardButton('/Start')
b1 = KeyboardButton('/время_работы')
b2 = KeyboardButton('/адрес')
b3 = KeyboardButton('/меню')


kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(b0).insert(b1).add(b2).insert(b3)

